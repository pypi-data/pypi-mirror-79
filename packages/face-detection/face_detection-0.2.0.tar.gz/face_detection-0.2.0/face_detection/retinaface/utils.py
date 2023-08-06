# Adapted from https://github.com/biubug6/Pytorch_Retinaface
# Original license: MIT
import torch


def decode_landm(pre, priors, variances):
    """Decode landm from predictions using priors to undo
    the encoding we did for offset regression at train time.
    Args:
        pre (tensor): landm predictions for loc layers,
            Shape: [N, num_priors,10]
        priors (tensor): Prior boxes in center-offset form.
            Shape: [num_priors,4].
        variances: (list[float]) Variances of priorboxes
    Return:
        decoded landm predictions
    """
    priors = priors[None]
    landms = torch.cat((priors[:, :, :2] + pre[:, :, :2] * variances[0] * priors[:, :, 2:],
                        priors[:, :, :2] + pre[:, :, 2:4] * variances[0] * priors[:, :, 2:],
                        priors[:, :, :2] + pre[:, :, 4:6] * variances[0] * priors[:, :, 2:],
                        priors[:, :, :2] + pre[:, :, 6:8] * variances[0] * priors[:, :, 2:],
                        priors[:, :, :2] + pre[:, :, 8:10] * variances[0] * priors[:, :, 2:],
                        ), dim=2)
    return landms
