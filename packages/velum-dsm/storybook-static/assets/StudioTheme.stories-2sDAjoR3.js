import{j as e,d as i}from"./iframe-v_xVpIIQ.js";import{S as s}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const x={title:"Tokens/StudioTheme"},r={render:()=>e.jsx(s,{maxWidth:"900px",children:e.jsx("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(220px, 1fr))",gap:"12px"},children:Object.entries(i).map(([t,d])=>e.jsxs("div",{style:{border:"1px solid var(--border)",borderRadius:"12px",padding:"16px",background:"var(--surface-strong)"},children:[e.jsx("div",{style:{fontWeight:700,marginBottom:"8px"},children:t}),e.jsx("div",{style:{fontFamily:"var(--velum-font-mono)",fontSize:"0.82rem",wordBreak:"break-word"},children:d})]},t))})})};var n,o,a;r.parameters={...r.parameters,docs:{...(n=r.parameters)==null?void 0:n.docs,source:{originalSource:`{
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
}`,...(a=(o=r.parameters)==null?void 0:o.docs)==null?void 0:a.source}}};const u=["Default"];export{r as Default,u as __namedExportsOrder,x as default};
