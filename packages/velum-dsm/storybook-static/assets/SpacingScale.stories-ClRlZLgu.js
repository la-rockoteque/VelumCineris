import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{O as o}from"./VelumProvider-Cnx-m3OC.js";import{S as d}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const v={title:"Tokens/SpacingScale"},n={render:()=>e.jsx(d,{children:e.jsx("div",{style:{border:"1px solid var(--border)",borderRadius:"12px",padding:"16px",background:"var(--surface-strong)"},children:Object.entries(o).map(([r,a])=>e.jsxs("div",{style:{display:"grid",gridTemplateColumns:"64px 1fr",gap:"12px",alignItems:"center",marginBottom:"10px"},children:[e.jsx("div",{style:{fontFamily:"var(--velum-font-mono)"},children:r}),e.jsxs("div",{style:{display:"flex",alignItems:"center",gap:"12px"},children:[e.jsx("div",{style:{width:a,height:"10px",borderRadius:"999px",background:"var(--accent)"}}),e.jsx("span",{style:{fontFamily:"var(--velum-font-mono)"},children:a})]})]},r))})})};var t,s,i;n.parameters={...n.parameters,docs:{...(t=n.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => <StoryFrame>
      <div style={{
      border: "1px solid var(--border)",
      borderRadius: "12px",
      padding: "16px",
      background: "var(--surface-strong)"
    }}>
        {Object.entries(spacingScale).map(([step, value]) => <div key={step} style={{
        display: "grid",
        gridTemplateColumns: "64px 1fr",
        gap: "12px",
        alignItems: "center",
        marginBottom: "10px"
      }}>
            <div style={{
          fontFamily: "var(--velum-font-mono)"
        }}>{step}</div>
            <div style={{
          display: "flex",
          alignItems: "center",
          gap: "12px"
        }}>
              <div style={{
            width: value,
            height: "10px",
            borderRadius: "999px",
            background: "var(--accent)"
          }} />
              <span style={{
            fontFamily: "var(--velum-font-mono)"
          }}>{value}</span>
            </div>
          </div>)}
      </div>
    </StoryFrame>
}`,...(i=(s=n.parameters)==null?void 0:s.docs)==null?void 0:i.source}}};const g=["Default"];export{n as Default,g as __namedExportsOrder,v as default};
