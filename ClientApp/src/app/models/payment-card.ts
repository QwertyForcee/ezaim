export interface PaymentCard {
    number: string;
    csv: string;
    initials: string;
    valid_through: string;
    owner_id: number;
}