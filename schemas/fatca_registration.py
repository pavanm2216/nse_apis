from pydantic import BaseModel
from typing import Optional, List


class FATCADetail(BaseModel):
    pan_rp: Optional[str] = None
    pekrn: Optional[str] = None
    inv_name: Optional[str] = None
    dob: Optional[str] = None
    fr_name: Optional[str] = None
    sp_name: Optional[str] = None
    tax_status: Optional[str] = None
    data_src: Optional[str] = None
    addr_type: Optional[str] = None
    po_bir_inc: Optional[str] = None
    co_bir_inc: Optional[str] = None
    tax_res1: Optional[str] = None
    tpin1: Optional[str] = None
    id1_type: Optional[str] = None
    tax_res2: Optional[str] = None
    tpin2: Optional[str] = None
    id2_type: Optional[str] = None
    tax_res3: Optional[str] = None
    tpin3: Optional[str] = None
    id3_type: Optional[str] = None
    tax_res4: Optional[str] = None
    tpin4: Optional[str] = None
    id4_type: Optional[str] = None
    srce_wealt: Optional[str] = None
    corp_servs: Optional[str] = None
    inc_slab: Optional[str] = None
    net_worth: Optional[str] = None
    nw_date: Optional[str] = None
    pep_flag: Optional[str] = None
    occ_code: Optional[str] = None
    occ_type: Optional[str] = None
    exemp_code: Optional[str] = None
    ffi_drnfe: Optional[str] = None
    giin_no: Optional[str] = None
    spr_entity: Optional[str] = None
    giin_na: Optional[str] = None
    giin_exemc: Optional[str] = None
    nffe_catg: Optional[str] = None
    act_nfe_sc: Optional[str] = None
    nature_bus: Optional[str] = None
    rel_listed: Optional[str] = None
    exch_name: Optional[str] = None
    ubo_appl: Optional[str] = None
    ubo_count: Optional[str] = None
    ubo_name: Optional[str] = None
    ubo_pan: Optional[str] = None
    ubo_nation: Optional[str] = None
    ubo_add1: Optional[str] = None
    ubo_add2: Optional[str] = None
    ubo_add3: Optional[str] = None
    ubo_city: Optional[str] = None
    ubo_pin: Optional[str] = None
    ubo_state: Optional[str] = None
    ubo_cntry: Optional[str] = None
    ubo_add_ty: Optional[str] = None
    ubo_ctr: Optional[str] = None
    ubo_tin: Optional[str] = None
    ubo_id_ty: Optional[str] = None
    ubo_cob: Optional[str] = None
    ubo_dob: Optional[str] = None
    ubo_gender: Optional[str] = None
    ubo_fr_nam: Optional[str] = None
    ubo_occ: Optional[str] = None
    ubo_occ_ty: Optional[str] = None
    ubo_tel: Optional[str] = None
    ubo_mobile: Optional[str] = None
    ubo_code: Optional[str] = None
    ubo_hol_pc: Optional[str] = None
    ubo_categ: Optional[str] = None
    ubo_pep_fl: Optional[str] = None
    ubo_email: Optional[str] = None
    ubo_smo_de: Optional[str] = None
    sdf_flag: Optional[str] = None
    ubo_df: Optional[str] = None
    aadhaar_rp: Optional[str] = None
    new_change: Optional[str] = None
    log_name: Optional[str] = None
    filler1: Optional[str] = None
    filler2: Optional[str] = None
    reg_id: Optional[str] = None
    reg_status: Optional[str] = None
    reg_remark: Optional[str] = None


class FATCAUploadRequest(BaseModel):
    reg_details: List[FATCADetail]


class FATCAUploadResponse(BaseModel):
    reg_details: List[FATCADetail]
