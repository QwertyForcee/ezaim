import { AddressModel } from "./address-model";

export interface SignUpModel {
    personalDataTermsAgreement: boolean;
    email: string;
    phoneNumber: string;
    password: string;
    confirmPassword: string;

    name: string;
    surname: string;
    passportNumber: string;
    identificationNumber: string;
    issueDate: string;
    expiryDate: string;
    authority: string;
    nationality: string;

    sex: boolean;
    resident: boolean;
    birthDate: string;

    birthAddress: AddressModel,
    
    registrationAddress: AddressModel,
    residentialAddress: AddressModel,
    salary: number;
}