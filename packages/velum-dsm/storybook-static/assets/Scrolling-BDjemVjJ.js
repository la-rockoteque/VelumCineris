import{j as e,W as r,J as a,M as i,p as t,q as c}from"./iframe-v_xVpIIQ.js";import{useMDXComponents as l}from"./index-BWRf6rO3.js";import{M as d,C as h,S as m}from"./blocks-B-kO7tlb.js";import"./preload-helper-Dp1pzeXC.js";import"./index-D8ls08wW.js";function s(o){const n={h1:"h1",h2:"h2",li:"li",p:"p",ul:"ul",...l(),...o.components};return e.jsxs(e.Fragment,{children:[e.jsx(d,{title:"Patterns/Scrolling"}),`
`,e.jsx(n.h1,{id:"scrolling",children:"Scrolling"}),`
`,e.jsx(n.p,{children:"Horizontal scroll belongs to the content region, not the page. Keep tool chrome fixed and push overflow into the local data container."}),`
`,e.jsx(n.h2,{id:"contract",children:"Contract"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Use local overflow for wide datasets and previews."}),`
`,e.jsx(n.li,{children:"Preserve surrounding actions, filters, and headings outside the scroll region."}),`
`,e.jsx(n.li,{children:"Make the scroll boundary visually clear."}),`
`]}),`
`,e.jsx(h,{children:e.jsx(m,{name:"Scrollable Data Region",children:e.jsxs(r,{children:[e.jsx(a,{children:"Wide Dataset"}),e.jsx(i,{children:"Prefer local overflow instead of forcing page-level horizontal scroll."}),e.jsx(t,{children:e.jsx(c,{minWidth:"760px",onRowClick:()=>{},rows:[{name:"Magic Missile",source:"PHB",school:"Evocation",tag:"Ready"},{name:"Counterspell",source:"PHB",school:"Abjuration",tag:"Review"}],columns:[{key:"name",header:"Name"},{key:"source",header:"Source"},{key:"school",header:"School"},{key:"tag",header:"Status"}]})})]})})}),`
`,e.jsx(n.h2,{id:"recommended-use-cases",children:"Recommended Use Cases"}),`
`,e.jsxs(n.ul,{children:[`
`,e.jsx(n.li,{children:"Compendium and validation tables"}),`
`,e.jsx(n.li,{children:"Preview panes with many columns"}),`
`,e.jsx(n.li,{children:"Related-record sections in details views"}),`
`]})]})}function f(o={}){const{wrapper:n}={...l(),...o.components};return n?e.jsx(n,{...o,children:e.jsx(s,{...o})}):s(o)}export{f as default};
