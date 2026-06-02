export interface ApiErrorBody {
  detail: string | ValidationErrorItem[];
}

export interface ValidationErrorItem {
  loc: (string | number)[];
  msg: string;
  type: string;
}
