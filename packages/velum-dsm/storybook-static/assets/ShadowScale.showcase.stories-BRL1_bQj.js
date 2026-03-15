import{j as a,a as o}from"./iframe-v_xVpIIQ.js";import{S as i,a as c,b as p}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const g={title:"Tokens/ShadowScale"},e={render:()=>a.jsx(i,{maxWidth:"980px",children:a.jsx("div",{style:{padding:"24px",background:"radial-gradient(circle at top, rgba(195, 140, 91, 0.2), transparent 35%), var(--bg)"},children:a.jsx(c,{children:Object.entries(o).map(([r,t])=>a.jsx(p,{label:r,description:t,minHeight:"140px",children:a.jsx("div",{style:{padding:"24px",borderRadius:"16px",background:"var(--surface-strong)",boxShadow:t}})},r))})})})};var n,s,d;e.parameters={...e.parameters,docs:{...(n=e.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <div style={{
      padding: "24px",
      background: "radial-gradient(circle at top, rgba(195, 140, 91, 0.2), transparent 35%), var(--bg)"
    }}>
        <StateMatrix>
          {Object.entries(shadowScale).map(([token, value]) => <StateCase key={token} label={token} description={value} minHeight="140px">
              <div style={{
            padding: "24px",
            borderRadius: "16px",
            background: "var(--surface-strong)",
            boxShadow: value
          }} />
            </StateCase>)}
        </StateMatrix>
      </div>
    </StoryFrame>
}`,...(d=(s=e.parameters)==null?void 0:s.docs)==null?void 0:d.source}}};const S=["Showcase"];export{e as Showcase,S as __namedExportsOrder,g as default};
