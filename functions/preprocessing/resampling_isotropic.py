import functions.setting_utils as su
import SimpleITK as sitk
import functions.image_processing as ip


def resampling(data, spacing=None, requested_im_list=None):
    if spacing is None:
        spacing = [1, 1, 1]
    if requested_im_list is None:
        requested_im_list = ['Im']
    data_exp_dict = [{'data': data, 'deform_exp': '3D_max25_D12'}]
    setting = su.initialize_setting('')
    setting = su.load_setting_from_data_dict(setting, data_exp_dict)

    for type_im in range(len(setting['data'][data]['types'])):
        for cn in setting['data'][data]['CNList']:
            im_info_su = {'data': data, 'type_im': type_im, 'cn': cn}
            for requested_im in requested_im_list:
                if requested_im == 'Im':
                    interpolator = sitk.sitkBSpline
                elif requested_im in ['Mask', 'Torso']:
                    interpolator = sitk.sitkNearestNeighbor
                else:
                    raise ValueError('interpolator is only defined for ["Im", "Mask", "Torso"] not for '+requested_im)
                im_raw_sitk = sitk.ReadImage(su.address_generator(setting, 'original'+requested_im+'Raw', **im_info_su))
                im_sitk = ip.resampler_sitk(im_raw_sitk, spacing,
                                            default_pixel_value=setting['data'][data]['defaultPixelValue'],
                                            interpolator=interpolator,
                                            dimension=3)
                sitk.WriteImage(im_sitk, su.address_generator(setting, 'original'+requested_im, **im_info_su))


if __name__ == '__main__':
    resampling(data='DIR-Lab_4D', spacing=[1, 1, 1], requested_im_list=['Im', 'Mask', 'Torso'])