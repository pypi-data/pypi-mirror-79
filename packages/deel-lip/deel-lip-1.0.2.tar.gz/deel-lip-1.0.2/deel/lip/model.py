# Copyright IRT Antoine de Saint Exupéry et Université Paul Sabatier Toulouse III - All
# rights reserved. DEEL is a research program operated by IVADO, IRT Saint Exupéry,
# CRIAQ and ANITI - https://www.deel.ai/
# =====================================================================================
"""
This module contains equivalents for Model and Sequential. These classes add support
for condensation and vanilla exportation.
"""
import math
from warnings import warn
import numpy as np
from tensorflow.keras import Sequential as KerasSequential, Model as KerasModel
from tensorflow.keras.layers import Input
from .layers import LipschitzLayer, Condensable
from .utils import _deel_export


@_deel_export
class Sequential(KerasSequential, LipschitzLayer, Condensable):
    def __init__(
        self,
        layers=None,
        name=None,
        k_coef_lip=1.0,
    ):
        """
        Equivalent of keras.Sequential but allow to set k-lip factor globally. Also
        support condensation and vanilla exportation.
        For now constant repartition is implemented (each layer
        get n_sqrt(k_lip_factor), where n is the number of layers)
        But in the future other repartition function may be implemented.

        Args:
            layers: list of layers to add to the model.
            name: name of the model, can be None
            k_coef_lip: the Lipschitz coefficient to ensure globally on the model.
        """
        super().__init__(layers, name)
        self.set_klip_factor(k_coef_lip)

    def build(self, input_shape=None):
        self._init_lip_coef(input_shape)
        return super(Sequential, self).build(input_shape)

    def set_klip_factor(self, klip_factor):
        super(Sequential, self).set_klip_factor(klip_factor)
        nb_layers = np.sum([isinstance(layer, LipschitzLayer) for layer in self.layers])
        for layer in self.layers:
            if isinstance(layer, LipschitzLayer):
                layer.set_klip_factor(math.pow(klip_factor, 1 / nb_layers))
            else:
                warn(
                    "Sequential model contains a layer wich is not a Lipschitsz layer: {}".format(  # noqa: E501
                        layer.name
                    )
                )

    def _compute_lip_coef(self, input_shape=None):
        for layer in self.layers:
            if isinstance(layer, LipschitzLayer):
                layer._compute_lip_coef(input_shape)
            else:
                warn(
                    "Sequential model contains a layer wich is not a Lipschitsz layer: {}".format(  # noqa: E501
                        layer.name
                    )
                )

    def _init_lip_coef(self, input_shape):
        for layer in self.layers:
            if isinstance(layer, LipschitzLayer):
                layer._init_lip_coef(input_shape)
            else:
                warn(
                    "Sequential model contains a layer wich is not a Lipschitsz layer: {}".format(  # noqa: E501
                        layer.name
                    )
                )

    def _get_coef(self):
        global_coef = 1.0
        for layer in self.layers:
            if isinstance(layer, LipschitzLayer) and (global_coef is not None):
                global_coef *= layer._get_coef()
            else:
                warn(
                    "Sequential model contains a layer wich is not a Lipschitsz layer: {}".format(  # noqa: E501
                        layer.name
                    )
                )
                global_coef = None
        return global_coef

    def condense(self):
        for layer in self.layers:
            if isinstance(layer, Condensable):
                layer.condense()

    def vanilla_export(self):
        layers = list()
        for layer in self.layers:
            if isinstance(layer, Condensable):
                layer.condense()
                layers.append(layer.vanilla_export())
            else:
                lay_cp = layer.__class__.from_config(layer.get_config())
                lay_cp.build(layer.input.shape[1:])
                lay_cp.set_weights(layer.get_weights())
                layers.append(lay_cp)
        model = KerasSequential(layers, self.name)
        return model

    def get_config(self):
        config = {"k_coef_lip": self.k_coef_lip}
        base_config = super(Sequential, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


@_deel_export
class Model(KerasModel, Condensable):
    def __init__(self, *args, **kwargs):
        """
        Equivalent of keras.Model but support condensation and vanilla exportation.

        Warning:
             As lipschitz constant are multiplicative along layer, the Model class
             cannot set a global Lipschitz constant (problem with branching inside a
             model).
        """
        super().__init__(*args, **kwargs)

    def condense(self):
        for layer in self.layers:
            if isinstance(layer, Condensable):
                layer.condense()

    def vanilla_export(self):
        dict_src = {}
        input_l = Input(self.input.shape[1:])
        mdl = input_l
        dict_src[self.input.name] = mdl
        for lay in self.layers:
            if lay.input.name in dict_src:
                print("tensor input shape " + str(dict_src[lay.input.name].shape))
            if lay.input.name == lay.output.name:
                pass
            else:
                if isinstance(lay, Condensable):
                    lay.condense()
                    new_lay = lay.vanilla_export()
                    mdl = new_lay(dict_src[lay.input.name])
                else:
                    # duplicate layer (warning weights are not duplicated)
                    lay_cp = lay.__class__.from_config(lay.get_config())
                    lay_cp.build(lay.input.shape)
                    lay_cp.set_weights(lay.get_weights().copy())
                    mdl = lay_cp(dict_src[lay.input.name])
            dict_src[lay.output.name] = mdl
        net = KerasModel(input_l, mdl)
        return net


vanillaModel = Model.vanilla_export
