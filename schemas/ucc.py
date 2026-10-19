from pydantic import BaseModel, model_validator
from typing import Optional, List, Any


class UCCDetail(BaseModel):
    model_config = {"populate_by_name": True, "extra": "forbid"}

    client_code: Optional[str] = None
    primary_holder_first_name: Optional[str] = None
    primary_holder_middle_name: Optional[str] = None
    primary_holder_last_name: Optional[str] = None
    tax_status: Optional[str] = None
    gender: Optional[str] = None
    primary_holder_dob_incorporation: Optional[str] = None
    occupation_code: Optional[str] = None
    holding_nature: Optional[str] = None
    second_holder_first_name: Optional[str] = None
    second_holder_middle_name: Optional[str] = None
    second_holder_last_name: Optional[str] = None
    third_holder_first_name: Optional[str] = None
    third_holder_middle_name: Optional[str] = None
    third_holder_last_name: Optional[str] = None
    second_holder_dob: Optional[str] = None
    third_holder_dob: Optional[str] = None
    guardian_first_name: Optional[str] = None
    guardian_middle_name: Optional[str] = None
    guardian_last_name: Optional[str] = None
    guardian_dob: Optional[str] = None
    primary_holder_pan_exempt: Optional[str] = None
    second_holder_pan_exempt: Optional[str] = None
    third_holder_pan_exempt: Optional[str] = None
    guardian_pan_exempt: Optional[str] = None
    primary_holder_pan: Optional[str] = None
    second_holder_pan: Optional[str] = None
    third_holder_pan: Optional[str] = None
    guardian_pan: Optional[str] = None
    primary_holder_exempt_category: Optional[str] = None
    second_holder_exempt_category: Optional[str] = None
    third_holder_exempt_category: Optional[str] = None
    guardian_exempt_category: Optional[str] = None
    client_type: Optional[str] = None
    pms: Optional[str] = None
    default_dp: Optional[str] = None
    cdsl_dpid: Optional[str] = None
    cdslcltid: Optional[str] = None
    cmbp_id: Optional[str] = None
    nsdldpid: Optional[str] = None
    nsdlcltid: Optional[str] = None
    account_type_1: Optional[str] = None
    account_no_1: Optional[str] = None
    micr_no_1: Optional[str] = None
    ifsc_code_1: Optional[str] = None
    default_bank_flag_1: Optional[str] = None
    account_type_2: Optional[str] = None
    account_no_2: Optional[str] = None
    micr_no_2: Optional[str] = None
    ifsc_code_2: Optional[str] = None
    default_bank_flag_2: Optional[str] = None
    account_type_3: Optional[str] = None
    account_no_3: Optional[str] = None
    micr_no_3: Optional[str] = None
    ifsc_code_3: Optional[str] = None
    default_bank_flag_3: Optional[str] = None
    account_type_4: Optional[str] = None
    account_no_4: Optional[str] = None
    micr_no_4: Optional[str] = None
    ifsc_code_4: Optional[str] = None
    default_bank_flag_4: Optional[str] = None
    account_type_5: Optional[str] = None
    account_no_5: Optional[str] = None
    micr_no_5: Optional[str] = None
    ifsc_code_5: Optional[str] = None
    default_bank_flag_5: Optional[str] = None
    cheque_name: Optional[str] = None
    div_pay_mode: Optional[str] = None
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: Optional[str] = None
    resi_phone: Optional[str] = None
    resi_fax: Optional[str] = None
    office_phone: Optional[str] = None
    office_fax: Optional[str] = None
    email: Optional[str] = None
    communication_mode: Optional[str] = None
    foreign_address_1: Optional[str] = None
    foreign_address_2: Optional[str] = None
    foreign_address_3: Optional[str] = None
    foreign_address_city: Optional[str] = None
    foreign_address_pincode: Optional[str] = None
    foreign_address_state: Optional[str] = None
    foreign_address_country: Optional[str] = None
    foreign_address_resi_phone: Optional[str] = None
    foreign_address_fax: Optional[str] = None
    foreign_address_off_phone: Optional[str] = None
    foreign_address_off_fax: Optional[str] = None
    indian_mobile_no: Optional[str] = None
    primary_holder_kyc_type: Optional[str] = None
    primary_holder_ckyc_number: Optional[str] = None
    second_holder_kyc_type: Optional[str] = None
    second_holder_ckyc_number: Optional[str] = None
    third_holder_kyc_type: Optional[str] = None
    third_holder_ckyc_number: Optional[str] = None
    guardian_kyc_type: Optional[str] = None
    guardian_ckyc_number: Optional[str] = None
    primary_holder_kra_exempt_ref_no: Optional[str] = None
    second_holder_kra_exempt_ref_no: Optional[str] = None
    third_holder_kra_exempt_ref_no: Optional[str] = None
    guardian_exempt_ref_no: Optional[str] = None
    aadhaar_updated: Optional[str] = None
    mapin_id: Optional[str] = None
    paperless_flag: Optional[str] = None
    lei_no: Optional[str] = None
    lei_validity: Optional[str] = None
    mobile_declaration_flag: Optional[str] = None
    email_declaration_flag: Optional[str] = None
    second_holder_email: Optional[str] = None
    second_holder_email_declaration: Optional[str] = None
    second_holder_mobile: Optional[str] = None
    second_holder_mobile_declaration: Optional[str] = None
    third_holder_email: Optional[str] = None
    third_holder_email_declaration: Optional[str] = None
    third_holder_mobile: Optional[str] = None
    third_holder_mobile_declaration: Optional[str] = None
    guardian_relation: Optional[str] = None
    nomination_opt: Optional[str] = None
    nomination_authentication: Optional[str] = None
    nominee_1_name: Optional[str] = None
    nominee_1_relationship: Optional[str] = None
    nominee_1_applicable: Optional[Any] = None
    nominee_1_minor_flag: Optional[str] = None
    nominee_1_dob: Optional[str] = None
    nominee_1_guardian: Optional[str] = None
    nominee_1_guardian_pan: Optional[str] = None
    nominee_1_identity_type: Optional[str] = None
    nominee_1_identity_number: Optional[str] = None
    nominee_1_email: Optional[str] = None
    nominee_1_mobile: Optional[str] = None
    nominee_1_address1: Optional[str] = None
    nominee_1_address2: Optional[str] = None
    nominee_1_address3: Optional[str] = None
    nominee_1_city: Optional[str] = None
    nominee_1_pin: Optional[str] = None
    nominee_1_country: Optional[str] = None
    nominee_2_name: Optional[str] = None
    nominee_2_relationship: Optional[str] = None
    nominee_2_applicable: Optional[Any] = None
    nominee_2_minor_flag: Optional[str] = None
    nominee_2_dob: Optional[str] = None
    nominee_2_guardian: Optional[str] = None
    nominee_2_guardian_pan: Optional[str] = None
    nominee_2_identity_type: Optional[str] = None
    nominee_2_identity_number: Optional[str] = None
    nominee_2_email: Optional[str] = None
    nominee_2_mobile: Optional[str] = None
    nominee_2_address1: Optional[str] = None
    nominee_2_address2: Optional[str] = None
    nominee_2_address3: Optional[str] = None
    nominee_2_city: Optional[str] = None
    nominee_2_pin: Optional[str] = None
    nominee_2_country: Optional[str] = None
    nominee_3_name: Optional[str] = None
    nominee_3_relationship: Optional[str] = None
    nominee_3_applicable: Optional[Any] = None
    nominee_3_minor_flag: Optional[str] = None
    nominee_3_dob: Optional[str] = None
    nominee_3_guardian: Optional[str] = None
    nominee_3_guardian_pan: Optional[str] = None
    nominee_3_identity_type: Optional[str] = None
    nominee_3_identity_number: Optional[str] = None
    nominee_3_email: Optional[str] = None
    nominee_3_mobile: Optional[str] = None
    nominee_3_address1: Optional[str] = None
    nominee_3_address2: Optional[str] = None
    nominee_3_address3: Optional[str] = None
    nominee_3_city: Optional[str] = None
    nominee_3_pin: Optional[str] = None
    nominee_3_country: Optional[str] = None
    nominee_soa: Optional[str] = None
    reg_id: Optional[str] = None
    reg_status: Optional[str] = None
    reg_remark: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def strip_keys(cls, values: Any) -> Any:
        if isinstance(values, dict):
            return {k.strip(): v for k, v in values.items()}
        return values


class UCCDetailResponse(UCCDetail):
    """Same fields as UCCDetail but allows extra fields NSE may add in responses."""
    model_config = {"populate_by_name": True, "extra": "allow"}


class UCCRegistrationRequest(BaseModel):
    reg_details: List[UCCDetail]


class UCCRegistrationResponse(BaseModel):
    reg_details: Optional[List[UCCDetailResponse]] = None
    response_status: Optional[str] = None
    error_remark: Optional[str] = None

    model_config = {"extra": "allow"}
