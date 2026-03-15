import{j as e,W as a,J as c,U as o,V as l,X as d,k as h,G as x,b as s}from"./iframe-v_xVpIIQ.js";import{useMDXComponents as i}from"./index-BWRf6rO3.js";import{M as j,C as u,S as m}from"./blocks-B-kO7tlb.js";import"./preload-helper-Dp1pzeXC.js";import"./index-D8ls08wW.js";function t(r){const n={h1:"h1",h2:"h2",li:"li",p:"p",ul:"ul",...i(),...r.components};return e.jsxs(e.Fragment,{children:[e.jsx(j,{title:"Patterns/Error Management"}),`
`,e.jsx(n.h1,{id:"error-management",children:"Error Management"}),`
`,e.jsx(n.p,{children:"Errors should be specific, local to the failing surface, and recoverable."}),`
`,e.jsx(n.h2,{id:"contract",children:"Contract"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Place the error message inside the affected workspace or section."}),`
`,e.jsx(n.li,{children:"Explain the failure in concrete terms and suggest the next action."}),`
`,e.jsx(n.li,{children:"Keep retry and recovery actions adjacent to the error."}),`
`]}),`
`,e.jsx(u,{children:e.jsx(m,{name:"Recoverable Error",children:e.jsxs(a,{children:[e.jsx(c,{children:"Translator"}),e.jsxs(o,{children:[e.jsx(l,{children:"Error"}),e.jsx(d,{children:"The language context could not be loaded. Check the selected source sheet and retry."})]}),e.jsxs("label",{children:[e.jsx(n.p,{children:"Fallback Source"}),e.jsxs(h,{value:"dictionary",onChange:()=>{},children:[e.jsx("option",{value:"dictionary",children:"Dictionary"}),e.jsx("option",{value:"phonetics",children:"Phonetics"})]})]}),e.jsxs(x,{children:[e.jsx(s,{children:"Retry"}),e.jsx(s,{$variant:"ghost",children:"Open Logs"})]})]})})}),`
`,e.jsx(n.h2,{id:"recommended-use-cases",children:"Recommended Use Cases"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Failed API reads or writes"}),`
`,e.jsx(n.li,{children:"Missing validation sheets"}),`
`,e.jsx(n.li,{children:"Integration failures with partial success or retry semantics"}),`
`]})]})}function v(r={}){const{wrapper:n}={...i(),...r.components};return n?e.jsx(n,{...r,children:e.jsx(t,{...r})}):t(r)}export{v as default};
