import { useEffect, useMemo, useState } from "react";

import { Button, FeatureOutput, Toolbar, WorkspaceCard, WorkspaceLead, WorkspaceOutput, WorkspaceTitle } from "shared/library";
import type { MoneyCatalogResponse } from "shared/types/api";

interface MoneyTabProps {
  loading: boolean;
  moneyCatalog: MoneyCatalogResponse | null;
  onRefresh: () => Promise<void>;
}

export function MoneyTab(props: MoneyTabProps) {
  const [amount, setAmount] = useState("1");
  const [fromCurrency, setFromCurrency] = useState("");
  const [toCurrency, setToCurrency] = useState("");

  const currencies = props.moneyCatalog?.currencies || [];
  const matrix = props.moneyCatalog?.matrix || {};

  useEffect(() => {
    if (!currencies.length) {
      setFromCurrency("");
      setToCurrency("");
      return;
    }

    setFromCurrency((current) => (current && currencies.includes(current) ? current : currencies[0] || ""));
    setToCurrency((current) => {
      if (current && currencies.includes(current)) {
        return current;
      }
      return currencies[Math.min(1, currencies.length - 1)] || currencies[0] || "";
    });
  }, [currencies]);

  const conversion = useMemo(() => {
    const numericAmount = Number(amount || 0);
    if (!Number.isFinite(numericAmount)) {
      return "Enter a valid amount.";
    }
    if (!fromCurrency || !toCurrency) {
      return "Select currencies.";
    }
    if (fromCurrency === toCurrency) {
      return `${numericAmount.toFixed(2)} ${fromCurrency} = ${numericAmount.toFixed(2)} ${toCurrency}`;
    }

    const direct = Number(matrix[fromCurrency]?.[toCurrency]);
    if (Number.isFinite(direct) && direct > 0) {
      return `${numericAmount.toFixed(2)} ${fromCurrency} = ${(numericAmount * direct).toFixed(2)} ${toCurrency} (rate ${direct})`;
    }

    const reverse = Number(matrix[toCurrency]?.[fromCurrency]);
    if (Number.isFinite(reverse) && reverse > 0) {
      return `${numericAmount.toFixed(2)} ${fromCurrency} = ${(numericAmount / reverse).toFixed(2)} ${toCurrency} (derived rate ${(1 / reverse).toFixed(6)})`;
    }

    return `No conversion rate found between ${fromCurrency} and ${toCurrency}.`;
  }, [amount, fromCurrency, matrix, toCurrency]);

  return (
    <WorkspaceCard>
      <WorkspaceTitle>Money</WorkspaceTitle>
      <WorkspaceLead>Convert values across currencies using the money matrix from spreadsheet data.</WorkspaceLead>

      <Toolbar>
        <label>
          Amount
          <input type="number" step="any" value={amount} onChange={(event) => setAmount(event.target.value)} disabled={props.loading} />
        </label>

        <label>
          From
          <select value={fromCurrency} onChange={(event) => setFromCurrency(event.target.value)} disabled={props.loading || !currencies.length}>
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>

        <label>
          To
          <select value={toCurrency} onChange={(event) => setToCurrency(event.target.value)} disabled={props.loading || !currencies.length}>
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>

        <label>
          Refresh
          <Button disabled={props.loading} onClick={() => void props.onRefresh()}>
            Reload Matrix
          </Button>
        </label>
      </Toolbar>

      <FeatureOutput>{conversion}</FeatureOutput>
      <WorkspaceOutput>{JSON.stringify(matrix, null, 2)}</WorkspaceOutput>
    </WorkspaceCard>
  );
}
