import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{useMDXComponents as p}from"./index-B6-HLlhV.js";import{M as m,C as i,S as a}from"./index-BF7p2nz2.js";import{W as t,s as l,t as j,p as c,q as o,r as h,m as d,b as s,n as x,i as g,j as b,l as w}from"./VelumProvider-Cnx-m3OC.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";import"./iframe-DSOl_dEh.js";import"./index-BeIcEJ__.js";import"./index-DgH-xKnr.js";import"./index-DrFu-skq.js";function u(r){const n={code:"code",h1:"h1",h2:"h2",li:"li",p:"p",ul:"ul",...p(),...r.components};return e.jsxs(e.Fragment,{children:[e.jsx(m,{title:"Patterns/Operational States"}),`
`,e.jsx(n.h1,{id:"operational-states",children:"Operational States"}),`
`,e.jsx(n.p,{children:"These are the default interaction patterns for async and high-friction flows in Velum DSM. The goal is consistency across tools and apps, especially where users need to understand whether the interface is loading, scrollable, paginated, saving, disabled, or in error."}),`
`,e.jsx(n.h2,{id:"standard-contract",children:"Standard Contract"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Keep layout stable while state changes. Replace content, not the surrounding structure."}),`
`,e.jsx(n.li,{children:"Show status near the affected region. Do not force users to scan the whole page for feedback."}),`
`,e.jsx(n.li,{children:"Pair disabled controls with reason text when the reason is not obvious from context."}),`
`,e.jsx(n.li,{children:"Keep recovery actions adjacent to the state they resolve: retry near errors, save near edited content, pagination near the dataset."}),`
`,e.jsxs(n.li,{children:["Use ",e.jsx(n.code,{children:"MetaText"})," for secondary status copy and ",e.jsx(n.code,{children:"InsetCard"})," for contained state messaging."]}),`
`]}),`
`,e.jsx(n.h2,{id:"loading",children:"Loading"}),`
`,e.jsx(n.p,{children:"Use the same card shell, preserve form/table height where possible, and disable write actions while work is in flight."}),`
`,e.jsx(i,{children:e.jsx(a,{name:"Loading State",children:e.jsxs(t,{children:[e.jsx(l,{children:"Compendium Sync"}),e.jsx(j,{children:"Keep the current layout visible and communicate status in place."}),e.jsxs(c,{children:[e.jsx(o,{children:"Loading"}),e.jsx(h,{children:"Fetching rows from the selected sheet. Controls remain visible but write actions are paused."})]}),e.jsxs(d,{children:[e.jsx(s,{disabled:!0,children:"Refresh"}),e.jsx(s,{$variant:"primary",disabled:!0,children:e.jsx(n.p,{children:"Publish"})})]})]})})}),`
`,e.jsx(n.p,{children:"Recommended use cases:"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Initial data fetch for a workspace card"}),`
`,e.jsx(n.li,{children:"Reloading validation catalogs or translator context"}),`
`,e.jsx(n.li,{children:"Background refresh after a filter or source switch"}),`
`]}),`
`,e.jsx(n.h2,{id:"scrolling",children:"Scrolling"}),`
`,e.jsxs(n.p,{children:["Horizontal scroll belongs to the content region, not the page. Wrap wide datasets in ",e.jsx(n.code,{children:"TableWrap"})," so the shell and surrounding controls stay fixed."]}),`
`,e.jsx(i,{children:e.jsx(a,{name:"Scrollable Data Region",children:e.jsxs(t,{children:[e.jsx(l,{children:"Wide Dataset"}),e.jsx(x,{children:"Prefer local overflow instead of forcing page-level horizontal scroll."}),e.jsx(g,{children:e.jsx(b,{minWidth:"760px",rows:[{name:"Magic Missile",source:"PHB",school:"Evocation",tag:"Ready"},{name:"Counterspell",source:"PHB",school:"Abjuration",tag:"Review"}],columns:[{key:"name",header:"Name"},{key:"source",header:"Source"},{key:"school",header:"School"},{key:"tag",header:"Status"}]})})]})})}),`
`,e.jsx(n.p,{children:"Recommended use cases:"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Compendium and validation tables"}),`
`,e.jsx(n.li,{children:"Preview panes with many columns"}),`
`,e.jsx(n.li,{children:"Related-record sections in details views"}),`
`]}),`
`,e.jsx(n.h2,{id:"pagination",children:"Pagination"}),`
`,e.jsx(n.p,{children:"Pagination metadata and controls should sit directly below the dataset, with the current range or page count visible at all times."}),`
`,e.jsx(i,{children:e.jsx(a,{name:"Pagination Contract",children:e.jsxs(t,{children:[e.jsx(l,{children:"Paginated Results"}),e.jsx(x,{children:"Page 3 of 12 · 241 total rows"}),e.jsxs(d,{children:[e.jsx(s,{children:"Prev"}),e.jsx(s,{$variant:"primary",children:"Next"})]})]})})}),`
`,e.jsx(n.p,{children:"Recommended use cases:"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Server-backed row browsing"}),`
`,e.jsx(n.li,{children:"Log/history pages"}),`
`,e.jsx(n.li,{children:"Search results with stable result counts"}),`
`]}),`
`,e.jsx(n.h2,{id:"saving",children:"Saving"}),`
`,e.jsx(n.p,{children:"Saving states should preserve edit context. Keep the form active when safe, show the save phase in text, and disable only actions that would conflict with the current write."}),`
`,e.jsx(i,{children:e.jsx(a,{name:"Saving State",children:e.jsxs(t,{children:[e.jsx(l,{children:"Details Editor"}),e.jsx(j,{children:"Users should keep their bearings while a save is underway."}),e.jsxs("label",{children:[e.jsx(n.p,{children:"Name"}),e.jsx(w,{value:"Arcane Beacon",readOnly:!0})]}),e.jsxs(c,{children:[e.jsx(o,{children:"Saving"}),e.jsx(h,{children:"Writing changes to the selected row and syncing dependent fields."})]}),e.jsxs(d,{children:[e.jsx(s,{disabled:!0,children:"Discard"}),e.jsx(s,{$variant:"primary",disabled:!0,children:e.jsx(n.p,{children:"Saving..."})})]})]})})}),`
`,e.jsx(n.p,{children:"Recommended use cases:"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Record editors with autosave or manual publish"}),`
`,e.jsx(n.li,{children:"Mutation flows with linked-field synchronization"}),`
`,e.jsx(n.li,{children:"Integration actions that have a dry-run and live mode"}),`
`]}),`
`,e.jsx(n.h2,{id:"disabled",children:"Disabled"}),`
`,e.jsx(n.p,{children:"Disabled controls need surrounding context so the user understands what prerequisite is missing."}),`
`,e.jsx(i,{children:e.jsx(a,{name:"Disabled With Reason",children:e.jsxs(t,{children:[e.jsx(l,{children:"Image Generator"}),e.jsx(x,{children:"Select a row before generating prompts or artwork."}),e.jsxs(d,{children:[e.jsx(s,{disabled:!0,children:"Generate Prompt"}),e.jsx(s,{$variant:"primary",disabled:!0,children:e.jsx(n.p,{children:"Generate Image"})})]})]})})}),`
`,e.jsx(n.p,{children:"Recommended use cases:"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Actions that require row selection"}),`
`,e.jsx(n.li,{children:"Submit buttons gated on validation"}),`
`,e.jsx(n.li,{children:"Integrations blocked by missing credentials or settings"}),`
`]}),`
`,e.jsx(n.h2,{id:"error-management",children:"Error Management"}),`
`,e.jsx(n.p,{children:"Errors should be specific, local to the failing surface, and recoverable. Use a contained state card plus a direct retry path."}),`
`,e.jsx(i,{children:e.jsx(a,{name:"Recoverable Error",children:e.jsxs(t,{children:[e.jsx(l,{children:"Translator"}),e.jsxs(c,{children:[e.jsx(o,{children:"Error"}),e.jsx(h,{children:"The language context could not be loaded. Check the selected source sheet and retry."})]}),e.jsxs(d,{children:[e.jsx(s,{children:"Retry"}),e.jsx(s,{$variant:"ghost",children:"Open Logs"})]})]})})}),`
`,e.jsx(n.p,{children:"Recommended use cases:"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Failed API reads or writes"}),`
`,e.jsx(n.li,{children:"Missing validation sheets"}),`
`,e.jsx(n.li,{children:"Integration failures with partial success or retry semantics"}),`
`]})]})}function I(r={}){const{wrapper:n}={...p(),...r.components};return n?e.jsx(n,{...r,children:e.jsx(u,{...r})}):u(r)}export{I as default};
