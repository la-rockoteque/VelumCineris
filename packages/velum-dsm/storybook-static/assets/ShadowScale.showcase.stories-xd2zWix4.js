import{j as a}from"./jsx-runtime-Bll8AAhy.js";import{L as d}from"./VelumProvider-Cnx-m3OC.js";import{S as i,a as p,b as c}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const b={title:"Tokens/ShadowScale"},e={render:()=>a.jsx(i,{maxWidth:"980px",children:a.jsx("div",{style:{padding:"24px",background:"radial-gradient(circle at top, rgba(195, 140, 91, 0.2), transparent 35%), var(--bg)"},children:a.jsx(p,{children:Object.entries(d).map(([r,t])=>a.jsx(c,{label:r,description:t,minHeight:"140px",children:a.jsx("div",{style:{padding:"24px",borderRadius:"16px",background:"var(--surface-strong)",boxShadow:t}})},r))})})})};var n,s,o;e.parameters={...e.parameters,docs:{...(n=e.parameters)==null?void 0:n.docs,source:{originalSource:`{
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
}`,...(o=(s=e.parameters)==null?void 0:s.docs)==null?void 0:o.source}}};const h=["Showcase"];export{e as Showcase,h as __namedExportsOrder,b as default};
