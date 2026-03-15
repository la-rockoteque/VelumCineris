import{j as e,c as l}from"./iframe-v_xVpIIQ.js";import{S as p}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const g={title:"Tokens/ColorFamilies"},r={render:()=>e.jsx(p,{maxWidth:"1100px",children:e.jsx("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(180px, 1fr))",gap:"16px"},children:Object.entries(l).map(([n,o])=>e.jsxs("div",{style:{border:"1px solid var(--border)",borderRadius:"12px",padding:"16px",background:"var(--surface-strong)"},children:[e.jsx("div",{style:{fontWeight:700,marginBottom:"12px",textTransform:"capitalize"},children:n}),e.jsx("div",{style:{display:"grid",gap:"8px"},children:Object.entries(o).map(([i,a])=>e.jsxs("div",{style:{display:"grid",gridTemplateColumns:"64px 1fr",gap:"12px",alignItems:"center"},children:[e.jsx("div",{style:{height:"32px",borderRadius:"8px",background:a,border:"1px solid var(--border)"}}),e.jsxs("div",{style:{fontFamily:"var(--velum-font-mono)",fontSize:"0.82rem"},children:[i,": ",a]})]},i))})]},n))})})};var t,s,d;r.parameters={...r.parameters,docs:{...(t=r.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1100px">
      <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
      gap: "16px"
    }}>
        {Object.entries(colorFamilies).map(([family, values]) => <div key={family} style={{
        border: "1px solid var(--border)",
        borderRadius: "12px",
        padding: "16px",
        background: "var(--surface-strong)"
      }}>
            <div style={{
          fontWeight: 700,
          marginBottom: "12px",
          textTransform: "capitalize"
        }}>{family}</div>
            <div style={{
          display: "grid",
          gap: "8px"
        }}>
              {Object.entries(values).map(([tone, swatch]) => <div key={tone} style={{
            display: "grid",
            gridTemplateColumns: "64px 1fr",
            gap: "12px",
            alignItems: "center"
          }}>
                  <div style={{
              height: "32px",
              borderRadius: "8px",
              background: swatch,
              border: "1px solid var(--border)"
            }} />
                  <div style={{
              fontFamily: "var(--velum-font-mono)",
              fontSize: "0.82rem"
            }}>
                    {tone}: {swatch}
                  </div>
                </div>)}
            </div>
          </div>)}
      </div>
    </StoryFrame>
}`,...(d=(s=r.parameters)==null?void 0:s.docs)==null?void 0:d.source}}};const v=["Default"];export{r as Default,v as __namedExportsOrder,g as default};
