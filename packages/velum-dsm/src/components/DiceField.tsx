import type {ChangeEvent} from "react";
import {useMemo} from "react";

import {styled} from "../styletron";

import {SelectInput, TextInput} from "./Inputs";

interface ParsedDiceValue {
    count: number;
    diceType: number;
    bonus: number;
}

const DEFAULT_DICE_TYPES = [4, 6, 8, 10, 12, 20, 100];

function parseDiceValue(rawValue: string): ParsedDiceValue {
    const match = rawValue.match(/^\s*(\d+)\s*d\s*(\d+)\s*([+-]\s*\d+)?\s*$/i);
    if (!match) {
        return {count: 0, diceType: 0, bonus: 0};
    }

    return {
        count: Number(match[1] || 0),
        diceType: Number(match[2] || 0),
        bonus: Number(String(match[3] || "0").replace(/\s+/g, "")) || 0,
    };
}

function safeNumber(value: string, fallback = 0): number {
    const next = Number(value);
    return Number.isFinite(next) ? next : fallback;
}

function stringifyDiceValue(input: ParsedDiceValue): string {
    if (!Number.isFinite(input.count) || input.count <= 0 || !Number.isFinite(input.diceType) || input.diceType <= 0) {
        return "";
    }

    const normalizedBonus = Number.isFinite(input.bonus) ? Math.trunc(input.bonus) : 0;
    const plus = normalizedBonus !== 0 ? (normalizedBonus > 0 ? `+${normalizedBonus}` : `${normalizedBonus}`) : "";
    return `${Math.floor(input.count)}d${Math.floor(input.diceType)}${plus}`;
}

export interface DiceFieldProps {
    value: string;
    onChange: (next: string) => void;
    className?: string;
    diceTypes?: number[];
}

const Root = styled("div", {
    display: "inline-flex",
});

const Token = styled("span", {
    minWidth: "10px",
    padding: "10px 12px",
    border: "1px solid var(--velum-color-border)",
    background: "rgba(255, 255, 255, 0.5)",
    color: "var(--velum-color-ink-soft)",
    fontSize: "var(--velum-font-size-xs)",
    fontWeight: 700,
    textAlign: "center",
});

export function DiceField(props: DiceFieldProps) {
    const parsed = useMemo(() => parseDiceValue(props.value), [props.value]);
    const diceTypeOptions = useMemo(() => {
        const base = props.diceTypes?.length ? props.diceTypes : DEFAULT_DICE_TYPES;
        const merged = parsed.diceType > 0 ? [...base, parsed.diceType] : [...base];
        return Array.from(new Set(merged)).sort((left, right) => left - right);
    }, [parsed.diceType, props.diceTypes]);

    const onCountChange = (event: ChangeEvent<HTMLInputElement>) => {
        props.onChange(stringifyDiceValue({...parsed, count: safeNumber(event.target.value, 0)}));
    };

    const onDiceTypeChange = (event: ChangeEvent<HTMLSelectElement>) => {
        props.onChange(stringifyDiceValue({...parsed, diceType: safeNumber(event.target.value, 0)}));
    };

    const onBonusChange = (event: ChangeEvent<HTMLInputElement>) => {
        props.onChange(stringifyDiceValue({...parsed, bonus: safeNumber(event.target.value, 0)}));
    };

    return (
        <Root className={props.className}>
            <TextInput
                style={{
                    width: "5rem",
                    borderTopRightRadius: 0,
                    borderBottomRightRadius: 0,
                }}
                type="number"
                value={parsed.count ? String(parsed.count) : ""}
                placeholder="Count"
                min={1}
                step={1}
                onChange={onCountChange}
            />
            <SelectInput
                style={{
                    width: "3.5rem",
                    borderRadius: 0,
                }}
                aria-label="Dice type"
                value={parsed.diceType ? String(parsed.diceType) : ""}
                onChange={onDiceTypeChange}
            >
                <option value=""/>
                {diceTypeOptions.map((diceType) => (
                    <option key={diceType} value={diceType}>
                        d{diceType}
                    </option>
                ))}
            </SelectInput>
            <TextInput
                style={{
                    width: "3.8rem",
                    borderTopLeftRadius: 0,
                    borderBottomLeftRadius: 0,
                }}
                type="number"
                value={parsed.bonus ? String(parsed.bonus) : ""}
                placeholder="Bonus"
                step={1}
                onChange={onBonusChange}
            />
        </Root>
    );
}
