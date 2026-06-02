import { useState } from "react";
import { PoliciesSection } from "./components/PoliciesSection";
import { SummarySection } from "./components/SummarySection";
import { usePortfolio } from "./hooks/usePortfolio";
import type { Policy } from "./types/policy";
import "./styles/app.css";
import "./styles/summary.css";
import "./styles/policies.css";
import "./styles/modal.css";
import "./styles/badges.css";

export function App() {
  const {
    summary,
    policies,
    actionTypes,
    summaryLoading,
    policiesLoading,
    summaryError,
    policiesError,
    actionTypesError,
    refetchAll,
  } = usePortfolio();

  const [selectedActionPolicy, setSelectedActionPolicy] =
    useState<Policy | null>(null);
  const [selectedRenewPolicy, setSelectedRenewPolicy] =
    useState<Policy | null>(null);

  return (
    <main className="app">
      <SummarySection
        summary={summary}
        loading={summaryLoading}
        error={summaryError}
      />

      <PoliciesSection
        policies={policies}
        actionTypes={actionTypes}
        loading={policiesLoading}
        error={policiesError}
        actionTypesError={actionTypesError}
        selectedActionPolicy={selectedActionPolicy}
        selectedRenewPolicy={selectedRenewPolicy}
        onRegisterAction={setSelectedActionPolicy}
        onRenew={setSelectedRenewPolicy}
        onCloseActionModal={() => setSelectedActionPolicy(null)}
        onCloseRenewModal={() => setSelectedRenewPolicy(null)}
        onMutationSuccess={refetchAll}
      />
    </main>
  );
}
