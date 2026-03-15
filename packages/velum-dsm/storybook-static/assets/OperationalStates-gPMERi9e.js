import{j as e}from"./iframe-v_xVpIIQ.js";import{useMDXComponents as s}from"./index-BWRf6rO3.js";import{M as a}from"./blocks-B-kO7tlb.js";import"./preload-helper-Dp1pzeXC.js";import"./index-D8ls08wW.js";function r(t){const n={code:"code",h1:"h1",h2:"h2",li:"li",p:"p",ul:"ul",...s(),...t.components};return e.jsxs(e.Fragment,{children:[e.jsx(a,{title:"Patterns/Operational States"}),`
`,e.jsx(n.h1,{id:"operational-states",children:"Operational States"}),`
`,e.jsx(n.p,{children:"These are the standard behavior patterns for async and high-friction flows in Velum DSM."}),`
`,e.jsx(n.h2,{id:"shared-contract",children:"Shared Contract"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Keep layout stable while state changes. Replace content, not the surrounding structure."}),`
`,e.jsx(n.li,{children:"Show status near the affected region. Do not force users to scan the whole page for feedback."}),`
`,e.jsx(n.li,{children:"Pair disabled controls with reason text when the reason is not obvious from context."}),`
`,e.jsx(n.li,{children:"Keep recovery actions adjacent to the state they resolve: retry near errors, save near edited content, pagination near the dataset."}),`
`,e.jsx(n.li,{children:"Use contained messaging for local feedback instead of global noise."}),`
`]}),`
`,e.jsx(n.h2,{id:"pattern-set",children:"Pattern Set"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:e.jsx(n.code,{children:"Patterns/Loading"})}),`
`,e.jsx(n.li,{children:e.jsx(n.code,{children:"Patterns/Scrolling"})}),`
`,e.jsx(n.li,{children:e.jsx(n.code,{children:"Patterns/Pagination"})}),`
`,e.jsx(n.li,{children:e.jsx(n.code,{children:"Patterns/Saving"})}),`
`,e.jsx(n.li,{children:e.jsx(n.code,{children:"Patterns/Disabled"})}),`
`,e.jsx(n.li,{children:e.jsx(n.code,{children:"Patterns/Error Management"})}),`
`]}),`
`,e.jsx(n.p,{children:"Use these as the baseline interaction contract across apps and tools."})]})}function h(t={}){const{wrapper:n}={...s(),...t.components};return n?e.jsx(n,{...t,children:e.jsx(r,{...t})}):r(t)}export{h as default};
