from __future__ import print_function, absolute_import, division

import tensorflow as tf


class BOMLOpt(tf.train.Optimizer):
    """
    mirror of the tf.train.Optimizer.
    """
    def minimize(
        self,
        loss_inner,
        var_list=None,
        global_step=None,
        gate_gradients=tf.train.Optimizer.GATE_OP,
        aggregation_method=None,
        colocate_gradients_with_ops=False,
        name=None,
        grad_loss=None,
    ):
        """ The `dynamics` contains a list of var_and_dynamics where var are both variables in `var_list` and also
        additional state (auxiliary) variables to be used in the process of back-propagation.
        """
        update_op, dynamics = super(BOMLOpt, self).minimize(
            loss_inner,
            global_step,
            var_list,
            gate_gradients,
            aggregation_method,
            colocate_gradients_with_ops,
            name,
            grad_loss,
        )
        return update_op, dynamics

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def learning_rate_tensor(self):
        return self._learning_rate_tensor

    @property
    def optimizer_params_tensor(self):
        return [self.learning_rate_tensor]
