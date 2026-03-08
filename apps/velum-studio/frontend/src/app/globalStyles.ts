import { css } from "@emotion/react";

export const globalStyles = css`
:root {
  --bg: #f8f6f1;
  --bg-alt: #efe8dc;
  --ink: #1f1e1b;
  --ink-soft: #585446;
  --accent: #9b4d1f;
  --accent-soft: #d88d5f;
  --surface: rgba(255, 251, 243, 0.88);
  --surface-strong: rgba(255, 250, 240, 0.96);
  --surface-muted: #f6eee2;
  --border: rgba(66, 48, 30, 0.18);
  --ok: #2b7a3f;
  --warn: #9a6b18;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  font-family: "IBM Plex Sans", "Trebuchet MS", sans-serif;
  color: var(--ink);
  background:
    radial-gradient(circle at 12% 10%, #fffaf0 0, #f4ecdf 45%, #eadfcd 100%),
    linear-gradient(140deg, #f2e8d8, #ead9c1);
  overflow-x: hidden;
}

.bg-shape {
  position: fixed;
  border-radius: 999px;
  filter: blur(44px);
  pointer-events: none;
  opacity: 0.45;
}

.bg-a {
  width: 380px;
  height: 380px;
  top: -80px;
  right: -120px;
  background: #ecb584;
}

.bg-b {
  width: 300px;
  height: 300px;
  bottom: -120px;
  left: -90px;
  background: #d6a37a;
}

.app-shell {
  max-width: 1440px;
  margin: 28px auto;
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--surface);
  backdrop-filter: blur(8px);
  animation: rise-in 320ms ease-out;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 16px;
}

.app-header h1 {
  margin: 0;
  font-family: "Avenir Next Condensed", "Franklin Gothic Medium", sans-serif;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.app-header p {
  margin: 6px 0 0;
  color: var(--ink-soft);
}

.pill {
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 7px 12px;
  font-size: 0.85rem;
  background: var(--surface-strong);
}

.pill.info {
  color: #5d513f;
  border-color: rgba(114, 83, 44, 0.28);
}

.pill.ok {
  color: var(--ok);
  border-color: rgba(43, 122, 63, 0.35);
}

.pill.warn {
  color: var(--warn);
  border-color: rgba(154, 107, 24, 0.35);
}

.app-header-status {
  display: grid;
  gap: 8px;
  justify-items: end;
}

.app-selection-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}

.global-loading {
  position: fixed;
  inset: 0;
  z-index: 160;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 14px;
  background: rgba(248, 239, 225, 0.74);
  backdrop-filter: blur(4px);
  font-size: 1.05rem;
  color: #4f4537;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 700;
}

.global-loading.hidden {
  display: none;
}

.global-loading-icon {
  flex: 0 0 auto;
  filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.14));
}

.error-banner {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid rgba(166, 53, 36, 0.4);
  border-radius: 10px;
  background: rgba(248, 224, 218, 0.95);
  color: #7b2e20;
  padding: 10px 12px;
  font-size: 0.86rem;
}

.error-banner.hidden {
  display: none;
}

.btn-inline {
  padding: 4px 10px;
  font-size: 0.78rem;
  white-space: nowrap;
}

.tabs {
  margin-top: 20px;
  display: grid;
  gap: 8px;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
}

.tab {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  background: var(--surface-strong);
  color: var(--ink-soft);
  font-weight: 700;
  cursor: pointer;
  transition: all 180ms ease;
}

.tab:hover,
.tab.active {
  color: var(--ink);
  border-color: rgba(155, 77, 31, 0.5);
  box-shadow: inset 0 -3px 0 var(--accent-soft);
}

.panel {
  margin-top: 16px;
  display: none;
}

.panel.active {
  display: block;
  animation: fade-in 240ms ease;
}

.panel-layout {
  display: grid;
  gap: 14px;
}

.workspace-card {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  background: var(--surface-strong);
}

.workspace-card h2 {
  margin: 0;
  font-family: "Avenir Next Condensed", "Trebuchet MS", sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.workspace-card p {
  margin: 6px 0 0;
  color: var(--ink-soft);
}

.workspace-grid {
  margin-top: 10px;
  display: grid;
  gap: 14px;
  grid-template-columns: minmax(260px, 360px) minmax(0, 1fr);
  align-items: start;
}

.workspace-controls {
  display: grid;
  gap: 10px;
  align-content: start;
}

.workspace-results {
  min-width: 0;
}

.toolbar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 10px;
  align-items: end;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.86rem;
  color: var(--ink-soft);
}

input,
textarea,
select,
.btn {
  border: 1px solid var(--border);
  border-radius: 9px;
  padding: 8px 10px;
  font: inherit;
  color: var(--ink);
  background: var(--surface-strong);
}

input:disabled,
textarea:disabled,
select:disabled,
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: rgba(155, 77, 31, 0.55);
  box-shadow: 0 0 0 2px rgba(155, 77, 31, 0.12);
}

textarea {
  resize: vertical;
}

.btn {
  cursor: pointer;
  font-weight: 600;
}

.btn:hover {
  border-color: rgba(155, 77, 31, 0.5);
}

.btn-loading {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-loading-label {
  letter-spacing: 0.02em;
}

.meta {
  margin-top: 8px;
  color: var(--ink-soft);
  min-height: 20px;
}

.meta.warn {
  color: var(--warn);
}

.table-wrap {
  margin-top: 12px;
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: auto;
  max-height: 60vh;
  background: var(--surface-strong);
}

.loading-parent {
  position: relative;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  z-index: 3;
  display: grid;
  place-content: center;
  gap: 8px;
  justify-items: center;
  backdrop-filter: blur(2px);
  background: rgba(250, 242, 231, 0.84);
  color: #5f5442;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.workspace-results .table-wrap,
.workspace-card > .table-wrap {
  margin-top: 0;
}

table {
  width: max-content;
  min-width: 100%;
  border-collapse: collapse;
}

th,
td {
  border-bottom: 1px solid rgba(66, 48, 30, 0.12);
  padding: 7px 8px;
  text-align: left;
  vertical-align: top;
  max-width: 340px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 0.88rem;
}

.row-actions-head,
.row-actions-cell {
  width: 280px;
  min-width: 280px;
}

th {
  position: sticky;
  top: 0;
  background: #f2e7d6;
  z-index: 1;
}

tr:hover td {
  background: #f9f0e5;
}

.row-clickable {
  cursor: pointer;
}

.row-selected td {
  background: #efe0cd;
}

.row-actions {
  display: flex;
  gap: 6px;
  justify-content: flex-end;
  align-items: center;
  opacity: 0;
  transform: translateX(8px);
  transition: opacity 140ms ease, transform 140ms ease;
}

tr:hover .row-actions,
.row-selected .row-actions {
  opacity: 1;
  transform: translateX(0);
}

.row-action-btn {
  padding: 4px 8px;
  font-size: 0.72rem;
  border-radius: 8px;
  min-width: 56px;
}

.row-action-menu {
  position: relative;
}

.row-action-menu > summary {
  list-style: none;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 4px 8px;
  font-size: 0.72rem;
  font-weight: 700;
  background: var(--surface-strong);
  cursor: pointer;
}

.row-action-menu > summary::-webkit-details-marker {
  display: none;
}

.row-action-menu-list {
  position: absolute;
  right: 0;
  top: calc(100% + 5px);
  z-index: 15;
  min-width: 110px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: #fff9ef;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.12);
  padding: 4px;
  display: grid;
  gap: 4px;
}

.row-action-menu-btn {
  border: 1px solid transparent;
  background: transparent;
  text-align: left;
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 0.76rem;
  cursor: pointer;
  color: #4f4537;
}

.row-action-menu-btn:hover {
  border-color: rgba(155, 77, 31, 0.35);
  background: #f6ecdd;
}

.pager {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}

.feature-output {
  margin-top: 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--surface-muted);
  padding: 10px;
  max-height: 42vh;
  overflow: auto;
  font-size: 0.8rem;
  white-space: pre-wrap;
}

.workspace-output {
  margin-top: 0;
  min-height: 320px;
}

.formatter-library-card,
.translator-card,
.translator-context-card {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #fbf5e8;
}

.formatter-library-card h3,
.translator-card h3,
.translator-context-card h3 {
  margin: 0 0 6px;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #6a5d4b;
}

.formatter-library-card p {
  margin: 0 0 8px;
  font-size: 0.8rem;
  color: var(--ink-soft);
}

.formatter-library-list {
  display: grid;
  gap: 6px;
}

.formatter-style-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.formatter-style-palette {
  display: grid;
  gap: 8px;
}

.style-palette-item {
  display: grid;
  grid-template-columns: minmax(120px, 1fr) 46px minmax(120px, 1fr);
  align-items: center;
  gap: 8px;
}

.style-palette-item > span {
  font-size: 0.76rem;
  color: #615543;
  font-weight: 700;
}

.style-palette-item input[type="color"] {
  width: 100%;
  min-height: 34px;
  padding: 3px;
}

.formatter-library-item {
  border: 1px solid rgba(66, 48, 30, 0.15);
  border-radius: 7px;
  background: #fff8ec;
  padding: 6px 8px;
  font-size: 0.78rem;
}

.translator-dual {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.translator-result {
  margin: 0;
  min-height: 78px;
  font-size: 0.82rem;
  white-space: pre-wrap;
}

.translator-context {
  display: grid;
  gap: 8px;
}

.translator-context-summary {
  font-size: 0.78rem;
  color: #6d5f4c;
}

.translator-context-block h4 {
  margin: 0 0 6px;
  font-size: 0.8rem;
  color: #5e513f;
}

.translator-context-block .table-wrap {
  margin-top: 0;
  max-height: 180px;
}

.translator-context-empty {
  font-size: 0.78rem;
  color: var(--ink-soft);
}

.timeline-months,
.timeline-weekdays,
.timeline-naming,
.timeline-holidays,
.timeline-era,
.timeline-present {
  display: grid;
  gap: 8px;
}

.timeline-month-card,
.timeline-naming-group,
.timeline-era-row,
.timeline-present-month {
  border: 1px solid rgba(66, 48, 30, 0.14);
  border-radius: 9px;
  background: #fff8eb;
  padding: 8px;
  overflow: hidden;
}

.timeline-month-card h4,
.timeline-naming-group h4 {
  margin: 0 0 6px;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: #655947;
}

.timeline-inline-input {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr);
  align-items: center;
  gap: 8px;
}

.timeline-inline-input > span {
  font-size: 0.76rem;
  color: #6a5f4d;
}

.timeline-holiday-row {
  display: grid;
  grid-template-columns: minmax(180px, 2fr) minmax(120px, 1fr) 84px 120px auto;
  gap: 8px;
  align-items: center;
}

.timeline-era-row {
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr) auto;
  gap: 8px;
  align-items: start;
  border-left: 4px solid rgba(66, 48, 30, 0.2);
}

.timeline-era-year {
  font-family: "Avenir Next Condensed", "Trebuchet MS", sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #5d513f;
}

.timeline-era-era {
  font-size: 0.76rem;
  color: #786b58;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.timeline-era-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.timeline-era-chip {
  font-size: 0.68rem;
  border: 1px solid rgba(66, 48, 30, 0.22);
  border-radius: 999px;
  padding: 1px 7px;
  color: #5f543f;
  background: rgba(255, 248, 236, 0.72);
}

.timeline-era-event {
  margin-top: 3px;
  font-size: 0.84rem;
  color: #4f4537;
}

.timeline-era-controls {
  display: grid;
  gap: 6px;
  justify-items: end;
}

.timeline-era-text {
  min-height: 56px;
  width: 100%;
}

.timeline-era-year-input {
  width: 100%;
}

.timeline-present {
  grid-template-columns: 1fr;
}

.timeline-present-header {
  display: grid;
  gap: 2px;
  margin-bottom: 6px;
}

.timeline-present-header h4 {
  margin: 0;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: #5f523f;
}

.timeline-present-year {
  font-size: 0.74rem;
  color: #7a6b57;
}

.timeline-present-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.72rem;
  table-layout: fixed;
}

.timeline-present-table th,
.timeline-present-table td {
  border: 1px solid rgba(66, 48, 30, 0.14);
  padding: 4px;
  vertical-align: top;
  width: 20%;
  max-width: none;
}

.timeline-present-table th {
  background: rgba(244, 230, 207, 0.55);
  color: #625543;
  font-weight: 700;
}

.timeline-present-day {
  font-weight: 700;
  color: #5a4d3b;
}

.timeline-present-cell {
  height: var(--timeline-day-height, 96px);
}

.timeline-present-event-list {
  display: grid;
  gap: 4px;
  margin-top: 4px;
}

.timeline-present-event {
  margin-top: 0;
  color: #6d5d48;
  white-space: pre-wrap;
  border: 1px solid rgba(66, 48, 30, 0.14);
  border-radius: 7px;
  background: rgba(244, 230, 207, 0.55);
  padding: 2px 5px;
}

.integration-actions {
  display: grid;
  gap: 8px;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
}

.integration-actions .btn {
  width: 100%;
}

.details-workspace {
  gap: 12px;
}

.details-shell {
  margin-top: 6px;
  display: grid;
  gap: 14px;
  grid-template-columns: minmax(280px, 360px) minmax(0, 1fr);
  align-items: start;
}

.details-sidebar {
  display: grid;
  gap: 10px;
  align-content: start;
  position: sticky;
  top: 12px;
}

.details-sidebar .meta {
  margin-top: 0;
}

.details-main {
  display: grid;
  gap: 12px;
  align-content: start;
  width: 100%;
  max-inline-size: min(1320px, calc(100vw - 440px));
}

.details-hero {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
  background: #f8efdf;
  display: grid;
  gap: 12px;
  grid-template-columns: minmax(0, 1fr) 260px;
  align-items: start;
}

.details-hero-info {
  display: grid;
  gap: 8px;
}

.details-hero-info h3 {
  margin: 0;
  font-family: "Avenir Next Condensed", "Trebuchet MS", sans-serif;
  font-size: 1.2rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.details-title-editable {
  cursor: pointer;
}

.details-title-editable:hover {
  color: var(--accent);
}

.details-hero-subtitle {
  margin: 0;
  color: var(--ink-soft);
  font-size: 0.86rem;
}

.details-hero-status {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.details-status-chip {
  border: 1px solid rgba(66, 48, 30, 0.16);
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 0.68rem;
  color: #6d624f;
  background: rgba(255, 249, 238, 0.78);
}

.details-hero-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.details-chip {
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.74rem;
  color: #5d513f;
  background: rgba(255, 250, 240, 0.9);
}

.details-media {
  border: 1px solid rgba(66, 48, 30, 0.24);
  border-radius: 10px;
  overflow: hidden;
  background: #efe2cf;
  min-height: 220px;
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
}

.details-media img {
  width: 100%;
  height: 100%;
  min-height: 180px;
  object-fit: cover;
  display: block;
}

.details-media-meta {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  align-items: center;
  padding: 8px 10px;
  background: rgba(255, 249, 238, 0.95);
  font-size: 0.72rem;
  color: #635744;
}

.details-media-meta a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 700;
}

.details-media-meta a:hover {
  text-decoration: underline;
}

.details-media-fallback {
  min-height: 220px;
  display: grid;
  place-items: center;
  text-align: center;
  font-size: 0.85rem;
  letter-spacing: 0.02em;
  color: #6b604f;
  padding: 12px;
}

.details-section {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
  background: #fbf4e7;
}

.details-section h3 {
  margin: 0;
  font-size: 0.88rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--ink-soft);
}

.details-section-grid {
  margin-top: 10px;
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 10px;
}

.field-item {
  grid-column: span 4;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.82rem;
  color: var(--ink-soft);
}

.field-item > span {
  font-size: 0.74rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: #645a49;
}

.field-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.field-abbrev-chip {
  font-style: normal;
  font-size: 0.66rem;
  font-weight: 700;
  text-transform: none;
  color: #756a56;
  border: 1px solid rgba(66, 48, 30, 0.16);
  border-radius: 999px;
  padding: 2px 8px;
  background: rgba(250, 242, 231, 0.92);
}

.field-checkbox {
  width: 18px;
  height: 18px;
}

.check-wrap {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 36px;
  font-size: 0.8rem;
  color: #5b4f3f;
}

.check-wrap input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin: 0;
}

.spell-components-editor,
.spell-savingthrow-editor,
.spell-measure-editor,
.spell-ability-trigger {
  display: grid;
  gap: 8px;
}

.spell-component-row {
  display: grid;
  gap: 8px;
  grid-template-columns: minmax(160px, 220px) minmax(0, 1fr);
  align-items: start;
}

.spell-component-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  color: #5e5240;
}

.spell-components-editor textarea.is-disabled {
  background: #f0e8dd;
  color: #887e6c;
}

.components-field {
  gap: 8px;
}

.components-option {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #5b4f3f;
}

.components-option-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 8px;
  align-items: center;
}

.components-note.is-disabled {
  background: #f0e8dd;
  color: #887e6c;
}

.spell-savingthrow-outcomes {
  display: grid;
  gap: 8px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.spell-savingthrow-item {
  display: grid;
  gap: 4px;
}

.spell-savingthrow-item > span {
  font-size: 0.72rem;
  color: #655a49;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.spell-measure-inline {
  display: grid;
  gap: 8px;
  grid-template-columns: minmax(80px, 110px) minmax(120px, 1fr) minmax(120px, 1fr);
}

.monster-ability-editor {
  display: inline-grid;
  grid-template-columns: minmax(70px, 110px) auto;
  align-items: center;
  gap: 8px;
}

.species-ability-editor {
  display: grid;
  grid-template-columns: minmax(110px, 1fr) minmax(70px, 110px);
  gap: 8px;
  align-items: center;
}

.pipe-entry-editor {
  display: grid;
  gap: 8px;
}

.line-item {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 8px;
}

.monster-ability-mod {
  border: 1px solid rgba(66, 48, 30, 0.16);
  border-radius: 7px;
  padding: 7px 10px;
  background: #f2e8d9;
  font-weight: 700;
  color: #5c5140;
  text-align: center;
  min-width: 52px;
}

.monster-linked-count {
  display: inline-grid;
  grid-template-columns: auto minmax(64px, 90px);
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.monster-linked-count > span {
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #615644;
}

.list-table-editor {
  display: grid;
  gap: 8px;
}

.list-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid rgba(66, 48, 30, 0.15);
  border-radius: 8px;
  overflow: hidden;
  background: #fffaf1;
}

.list-table th,
.list-table td {
  border-bottom: 1px solid rgba(66, 48, 30, 0.11);
  padding: 6px;
  font-size: 0.8rem;
}

.list-table th {
  position: static;
  background: #f4e8d8;
}

.list-table td:first-child,
.list-table th:first-child {
  width: 34px;
  text-align: center;
}

.list-table td:last-child,
.list-table th:last-child {
  width: 84px;
  text-align: right;
}

.multi-select {
  position: relative;
}

.multi-select-display {
  width: 100%;
  min-height: 36px;
  border: 1px solid rgba(66, 48, 30, 0.18);
  border-radius: 8px;
  background: #fffaf1;
  color: #4e4335;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  padding: 6px 8px;
  cursor: pointer;
  text-align: left;
}

.multi-select.is-open .multi-select-display {
  border-color: rgba(160, 110, 54, 0.55);
  box-shadow: 0 0 0 2px rgba(204, 165, 102, 0.2);
}

.multi-select-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  flex: 1;
}

.multi-select-pill {
  display: inline-flex;
  align-items: center;
  max-width: 100%;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid rgba(66, 48, 30, 0.16);
  background: rgba(241, 231, 214, 0.9);
  color: #5d503f;
  font-size: 0.72rem;
  line-height: 1.2;
}

.multi-select-placeholder {
  color: #8c7f6b;
  font-size: 0.76rem;
  line-height: 1.3;
}

.multi-select-caret {
  color: #6f634f;
  font-size: 0.8rem;
  line-height: 1.2;
  padding-top: 3px;
}

.multi-select-dropdown {
  position: absolute;
  z-index: 40;
  left: 0;
  right: 0;
  top: calc(100% + 4px);
  border: 1px solid rgba(66, 48, 30, 0.2);
  border-radius: 8px;
  background: #fffaf1;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  max-height: 220px;
  overflow: auto;
  padding: 6px;
}

.multi-select-options {
  display: grid;
  gap: 3px;
}

.multi-select-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 6px;
  border-radius: 6px;
  color: #4f4436;
  font-size: 0.8rem;
}

.multi-select-option:hover {
  background: rgba(234, 220, 195, 0.65);
}

.multi-select-option input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin: 0;
}

.select-with-loader {
  position: relative;
  padding-right: 30px;
}

.select-loading-indicator {
  position: absolute;
  right: 6px;
  bottom: 8px;
  pointer-events: none;
}

.field-span-full {
  grid-column: 1 / -1;
}

.field-editor-rich {
  min-height: 250px;
  line-height: 1.45;
}

.details-section--description textarea {
  min-height: 300px;
}

.relation-section {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
  background: #f7f0e5;
}

.relation-section h3 {
  margin: 0;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.relation-section .table-wrap {
  margin-top: 10px;
}

.component-checkboxes {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.component-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
  color: var(--ink);
}

.column-menu {
  position: fixed;
  z-index: 99;
  min-width: 220px;
  max-height: 60vh;
  overflow: auto;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--surface-strong);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  padding: 8px;
}

.column-menu.hidden {
  display: none;
}

.column-menu-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--ink-soft);
  margin-bottom: 6px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(66, 48, 30, 0.14);
}

.column-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
  color: var(--ink);
  font-size: 0.84rem;
}

.toast-host {
  position: fixed;
  right: 16px;
  bottom: 14px;
  z-index: 120;
  display: grid;
  gap: 8px;
  width: min(360px, calc(100vw - 24px));
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: rgba(255, 250, 240, 0.98);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.14);
  padding: 10px 12px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  align-items: start;
  animation: toast-in 180ms ease-out;
}

.toast-success {
  border-color: rgba(43, 122, 63, 0.35);
}

.toast-warning {
  border-color: rgba(154, 107, 24, 0.4);
}

.toast-info {
  border-color: rgba(47, 96, 112, 0.42);
}

.toast-error {
  border-color: rgba(166, 53, 36, 0.45);
}

.toast-text {
  font-size: 0.82rem;
  color: #4f4638;
}

.toast-close {
  border: 0;
  background: transparent;
  color: #73685a;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  line-height: 1;
  padding: 2px 4px;
}

.toast-close:hover {
  color: #463d30;
}

.toast-exit {
  animation: toast-out 200ms ease-in forwards;
}

.loader-visual {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.loader-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  animation: loader-bob 1100ms ease-in-out infinite;
}

.loader-visual--small {
  width: 18px;
  height: 18px;
}

.loader-visual--tiny {
  width: 14px;
  height: 14px;
}

.loader-visual--button {
  width: 18px;
  height: 18px;
}

.loader-visual--table {
  width: 56px;
  height: 56px;
}

.loader-visual--global {
  width: 190px;
  height: 190px;
}

.loader-fallback {
  position: absolute;
  width: 72%;
  height: 72%;
  border-radius: 50%;
  border: 3px solid rgba(155, 77, 31, 0.25);
  border-top-color: rgba(155, 77, 31, 0.85);
  animation: spin 820ms linear infinite;
}

.loader-visual.loader-ready .loader-fallback {
  display: none;
}

.loader-visual.loader-image-missing .loader-image {
  display: none;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes rise-in {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes loader-bob {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-5%) scale(1.02);
  }
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes toast-out {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(6px);
  }
}

@media (max-width: 1100px) {
  .workspace-grid,
  .details-shell {
    grid-template-columns: 1fr;
  }

  .translator-dual {
    grid-template-columns: 1fr;
  }

  .details-hero {
    grid-template-columns: 1fr;
  }

  .details-sidebar {
    position: static;
  }

  .details-main {
    max-inline-size: 100%;
  }

  .workspace-output {
    min-height: 220px;
  }
}

@media (max-width: 860px) {
  .app-shell {
    margin: 12px;
    padding: 14px;
    border-radius: 14px;
  }

  .app-header {
    flex-direction: column;
    align-items: stretch;
  }

  .app-header-status {
    justify-items: start;
  }

  .app-selection-pills {
    justify-content: flex-start;
  }

  .tabs {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }

  .toolbar {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }

  .field-item {
    grid-column: span 6;
  }

  .table-wrap {
    max-height: 52vh;
  }

  .row-actions {
    opacity: 1;
    transform: none;
  }

  .spell-component-row,
  .spell-savingthrow-outcomes,
  .spell-measure-inline {
    grid-template-columns: 1fr;
  }

  .timeline-holiday-row {
    grid-template-columns: 1fr 1fr;
  }

  .timeline-era-row {
    grid-template-columns: 1fr;
  }

  .timeline-era-controls {
    justify-items: start;
  }
}

@media (max-width: 560px) {
  .field-item {
    grid-column: 1 / -1;
  }

  .integration-actions {
    grid-template-columns: 1fr;
  }

  .timeline-holiday-row {
    grid-template-columns: 1fr;
  }
}
`;
