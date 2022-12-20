export interface LoanModel {
    id: number;
    status: number;
    amount: number;
    remaining_amount: number;
    created_at: string;
    percent: number;
    is_active: boolean;
}