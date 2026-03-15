import{j as e,W as r,J as l,K as d,T as o,n as c,U as h,V as u,X as x,G as j,b as i}from"./iframe-v_xVpIIQ.js";import{useMDXComponents as t}from"./index-BWRf6rO3.js";import{M as v,C as m,S as p}from"./blocks-B-kO7tlb.js";import"./preload-helper-Dp1pzeXC.js";import"./index-D8ls08wW.js";function a(s){const n={h1:"h1",h2:"h2",li:"li",p:"p",ul:"ul",...t(),...s.components};return e.jsxs(e.Fragment,{children:[e.jsx(v,{title:"Patterns/Saving"}),`
`,e.jsx(n.h1,{id:"saving",children:"Saving"}),`
`,e.jsx(n.p,{children:"Saving states should preserve edit context. Keep the form readable, show the phase of the save, and disable only conflicting actions."}),`
`,e.jsx(n.h2,{id:"contract",children:"Contract"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Leave field values visible while the save runs."}),`
`,e.jsx(n.li,{children:"Show save status close to the edited surface."}),`
`,e.jsx(n.li,{children:"Keep non-conflicting context readable so users do not lose orientation."}),`
`]}),`
`,e.jsx(m,{children:e.jsx(p,{name:"Saving State",children:e.jsxs(r,{children:[e.jsx(l,{children:"Details Editor"}),e.jsx(d,{children:"Users should keep their bearings while a save is underway."}),e.jsxs("label",{children:[e.jsx(n.p,{children:"Name"}),e.jsx(o,{value:"Arcane Beacon",readOnly:!0})]}),e.jsx(c,{ariaLabel:"Save mode",value:"dry_run",onChange:()=>{},options:[{value:"dry_run",label:"Dry Run"},{value:"live",label:"Live Execute",disabled:!0}]}),e.jsxs(h,{children:[e.jsx(u,{children:"Saving"}),e.jsx(x,{children:"Writing changes to the selected row and syncing dependent fields."})]}),e.jsxs(j,{children:[e.jsx(i,{disabled:!0,children:"Discard"}),e.jsx(i,{$variant:"primary",disabled:!0,children:e.jsx(n.p,{children:"Saving..."})})]})]})})}),`
`,e.jsx(n.h2,{id:"recommended-use-cases",children:"Recommended Use Cases"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Record editors with autosave or manual publish"}),`
`,e.jsx(n.li,{children:"Mutation flows with linked-field synchronization"}),`
`,e.jsx(n.li,{children:"Integration actions that have a dry-run and live mode"}),`
`]})]})}function w(s={}){const{wrapper:n}={...t(),...s.components};return n?e.jsx(n,{...s,children:e.jsx(a,{...s})}):a(s)}export{w as default};
