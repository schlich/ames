def tweak_ames(ames):
    def rating_to_num(df, col):
        return df[col].replace({'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1})
    
    return (ames
        .rename(columns=lambda c: c.lower().replace(' ', '_'))
        .assign(stories=lambda df_: df_.house_style.str.extract(r'(\d\.?\d?)').astype(float).fillna(0),
        has_bsmt=lambda df_:~df_.bsmt_qual.isna(),
        has_garage = lambda df_:~df_.garage_qual.isna(),
        **{k:lambda df_: rating_to_num(df_, k).fillna(0)
        for k in ['exter_qual', 'exter_cond', 'bsmt_qual', 'bsmt_cond', 'kitchen_qual', 'garage_qual',
        'garage_cond', 'heading_qc', 'fireplace_qu', 'pool_qc']},
        garage_yr_blt= lambda df_: df_.garage_yr_blt.fillna(df_.year_built).astype('uint8'),
        **{k: lambda df_, col=k:df_[col].fillna('Other').astype('category') for k in ['ms_zoning', 'street', 'alley', 'lot_shape', 'land_contour', 'utilities', 
        'lot_config', 'land_slope', 'neighborhood', 'condition_1', 'condition_2', 'bldg_type', 'house_style', 'roof_style', 'roof_matl', 'exterior_1st', 'exterior_2nd', 'mas_vn_type', 'foundation', 'bsmt_exposure', 'bsmtfin_type_1', 'bsmtfin_type_2', 'heating', 'electrical', 'functional', 'garage_type', 'garage_finish', 'paved_drive', 'fence', 'misc_feature', 'sale_type', 'sale_condition']},
        **{k: lambda df_, col=k:df_[col].fillna(0).astype(float) for k in ['lot_frontage', 'mas_vnr_area', 'bsmtfin_sf_1', 'bsmtfin_sf_2', 'bsmt_unf_sf', 'total_bsmt_sf', 'bsmt_full_bath', 'bsmt_half_bath', 'garage_cars', 'garage_area']},
        total_sf = lambda df_: df_.total_bsmt_sf + df_['1st_flr_sf'] + df_['2nd_flr_sf']

        ).astype({'central_air': bool,
        **{k:'uint8' for k in ['ms_subclass', 'overall_qual', 'overall_cond', 'full_bath', 'half_bath', 'bedroom_abvgr', 'kitchen_abvgr', 'totrms_abvgrd', 'fireplaces', 'mo_sold']},
        **{k:'uint16' for k in ['order', 'year_build', 'year_remod/add', '1st_flr_sf', '2nd_flr_sf', 'low_qual_fin_sf', 'gr_liv_area', 'wood_deck_sf', 'open_portch_sf', 'enclosed porch', '3ssn_porch', 'screen_porch', 'pool_area', 'yr_sold']},
        **{k: 'uint32' for k in ['lot_area', 'saleprice']},
        }).drop(columns=['pid'])
    )