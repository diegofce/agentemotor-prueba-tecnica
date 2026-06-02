import { useCallback, useEffect, useReducer } from "react";
import { fetchActionTypes } from "../api/actionTypes";
import { fetchPolicies } from "../api/policies";
import { fetchSummary } from "../api/summary";
import type { ActionType } from "../types/managementAction";
import type { Policy } from "../types/policy";
import type { Summary } from "../types/summary";

interface PortfolioState {
  summary: Summary | null;
  policies: Policy[];
  actionTypes: ActionType[];
  summaryLoading: boolean;
  policiesLoading: boolean;
  actionTypesLoading: boolean;
  summaryError: string | null;
  policiesError: string | null;
  actionTypesError: string | null;
}

type PortfolioAction =
  | { type: "SUMMARY_LOADING" }
  | { type: "SUMMARY_SUCCESS"; payload: Summary }
  | { type: "SUMMARY_ERROR"; payload: string }
  | { type: "POLICIES_LOADING" }
  | { type: "POLICIES_SUCCESS"; payload: Policy[] }
  | { type: "POLICIES_ERROR"; payload: string }
  | { type: "ACTION_TYPES_LOADING" }
  | { type: "ACTION_TYPES_SUCCESS"; payload: ActionType[] }
  | { type: "ACTION_TYPES_ERROR"; payload: string };

const initialState: PortfolioState = {
  summary: null,
  policies: [],
  actionTypes: [],
  summaryLoading: true,
  policiesLoading: true,
  actionTypesLoading: true,
  summaryError: null,
  policiesError: null,
  actionTypesError: null,
};

function portfolioReducer(
  state: PortfolioState,
  action: PortfolioAction,
): PortfolioState {
  switch (action.type) {
    case "SUMMARY_LOADING":
      return { ...state, summaryLoading: true, summaryError: null };
    case "SUMMARY_SUCCESS":
      return {
        ...state,
        summaryLoading: false,
        summary: action.payload,
        summaryError: null,
      };
    case "SUMMARY_ERROR":
      return {
        ...state,
        summaryLoading: false,
        summaryError: action.payload,
      };
    case "POLICIES_LOADING":
      return { ...state, policiesLoading: true, policiesError: null };
    case "POLICIES_SUCCESS":
      return {
        ...state,
        policiesLoading: false,
        policies: action.payload,
        policiesError: null,
      };
    case "POLICIES_ERROR":
      return {
        ...state,
        policiesLoading: false,
        policiesError: action.payload,
      };
    case "ACTION_TYPES_LOADING":
      return { ...state, actionTypesLoading: true, actionTypesError: null };
    case "ACTION_TYPES_SUCCESS":
      return {
        ...state,
        actionTypesLoading: false,
        actionTypes: action.payload,
        actionTypesError: null,
      };
    case "ACTION_TYPES_ERROR":
      return {
        ...state,
        actionTypesLoading: false,
        actionTypesError: action.payload,
      };
    default:
      return state;
  }
}

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    if (
      error.message === "Failed to fetch" ||
      error.message.includes("NetworkError")
    ) {
      return "No se pudo conectar con el backend. Inicie uvicorn en el puerto 8000.";
    }
    return error.message;
  }
  return "Ocurrió un error inesperado";
}

export function usePortfolio() {
  const [state, dispatch] = useReducer(portfolioReducer, initialState);

  const loadSummary = useCallback(async () => {
    dispatch({ type: "SUMMARY_LOADING" });
    try {
      const summary = await fetchSummary();
      dispatch({ type: "SUMMARY_SUCCESS", payload: summary });
    } catch (error: unknown) {
      dispatch({ type: "SUMMARY_ERROR", payload: getErrorMessage(error) });
    }
  }, []);

  const loadPolicies = useCallback(async () => {
    dispatch({ type: "POLICIES_LOADING" });
    try {
      const policies = await fetchPolicies();
      dispatch({ type: "POLICIES_SUCCESS", payload: policies });
    } catch (error: unknown) {
      dispatch({ type: "POLICIES_ERROR", payload: getErrorMessage(error) });
    }
  }, []);

  const loadActionTypes = useCallback(async () => {
    dispatch({ type: "ACTION_TYPES_LOADING" });
    try {
      const actionTypes = await fetchActionTypes();
      dispatch({ type: "ACTION_TYPES_SUCCESS", payload: actionTypes });
    } catch (error: unknown) {
      dispatch({
        type: "ACTION_TYPES_ERROR",
        payload: getErrorMessage(error),
      });
    }
  }, []);

  const refetchAll = useCallback(async () => {
    await Promise.all([loadSummary(), loadPolicies()]);
  }, [loadSummary, loadPolicies]);

  useEffect(() => {
    void loadActionTypes();
  }, [loadActionTypes]);

  useEffect(() => {
    void refetchAll();
  }, [refetchAll]);

  return {
    ...state,
    refetchAll,
  };
}
