import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{Q as d}from"./VelumProvider-Cnx-m3OC.js";import{S as s}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const v={title:"Tokens/StudioTheme"},r={render:()=>e.jsx(s,{maxWidth:"900px",children:e.jsx("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(220px, 1fr))",gap:"12px"},children:Object.entries(d).map(([t,i])=>e.jsxs("div",{style:{border:"1px solid var(--border)",borderRadius:"12px",padding:"16px",background:"var(--surface-strong)"},children:[e.jsx("div",{style:{fontWeight:700,marginBottom:"8px"},children:t}),e.jsx("div",{style:{fontFamily:"var(--velum-font-mono)",fontSize:"0.82rem",wordBreak:"break-word"},children:i})]},t))})})};var o,n,a;r.parameters={...r.parameters,docs:{...(o=r.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="900px">
      <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
      gap: "12px"
    }}>
        {Object.entries(studioTheme).map(([token, value]) => <div key={token} style={{
        border: "1px solid var(--border)",
        borderRadius: "12px",
        padding: "16px",
        background: "var(--surface-strong)"
      }}>
            <div style={{
          fontWeight: 700,
          marginBottom: "8px"
        }}>{token}</div>
            <div style={{
          fontFamily: "var(--velum-font-mono)",
          fontSize: "0.82rem",
          wordBreak: "break-word"
        }}>{value}</div>
          </div>)}
      </div>
    </StoryFrame>
}`,...(a=(n=r.parameters)==null?void 0:n.docs)==null?void 0:a.source}}};const c=["Default"];export{r as Default,c as __namedExportsOrder,v as default};
