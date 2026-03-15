import{j as e,W as a,J as o,M as l,G as d,b as t}from"./iframe-v_xVpIIQ.js";import{useMDXComponents as r}from"./index-BWRf6rO3.js";import{M as c,C as h,S as x}from"./blocks-B-kO7tlb.js";import"./preload-helper-Dp1pzeXC.js";import"./index-D8ls08wW.js";function i(s){const n={h1:"h1",h2:"h2",li:"li",p:"p",ul:"ul",...r(),...s.components};return e.jsxs(e.Fragment,{children:[e.jsx(c,{title:"Patterns/Disabled"}),`
`,e.jsx(n.h1,{id:"disabled",children:"Disabled"}),`
`,e.jsx(n.p,{children:"Disabled controls need surrounding context so the user understands what prerequisite is missing."}),`
`,e.jsx(n.h2,{id:"contract",children:"Contract"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Pair disabled controls with explicit reason text when the requirement is not obvious."}),`
`,e.jsx(n.li,{children:"Keep the explanation adjacent to the blocked action."}),`
`,e.jsx(n.li,{children:"Reserve disabled state for unavailable actions, not passive information."}),`
`]}),`
`,e.jsx(h,{children:e.jsx(x,{name:"Disabled With Reason",children:e.jsxs(a,{children:[e.jsx(o,{children:"Image Generator"}),e.jsx(l,{children:"Select a row before generating prompts or artwork."}),e.jsxs(d,{children:[e.jsx(t,{disabled:!0,children:"Generate Prompt"}),e.jsx(t,{$variant:"primary",disabled:!0,children:e.jsx(n.p,{children:"Generate Image"})})]})]})})}),`
`,e.jsx(n.h2,{id:"recommended-use-cases",children:"Recommended Use Cases"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Actions that require row selection"}),`
`,e.jsx(n.li,{children:"Submit buttons gated on validation"}),`
`,e.jsx(n.li,{children:"Integrations blocked by missing credentials or settings"}),`
`]})]})}function g(s={}){const{wrapper:n}={...r(),...s.components};return n?e.jsx(n,{...s,children:e.jsx(i,{...s})}):i(s)}export{g as default};
