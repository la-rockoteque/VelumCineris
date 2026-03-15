import{j as e,c as l}from"./iframe-v_xVpIIQ.js";import{S as m,a as p,b as x}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const v={title:"Tokens/ColorFamilies"},r={render:()=>e.jsx(m,{maxWidth:"1100px",children:e.jsx(p,{columns:"1fr",children:Object.entries(l).map(([t,o])=>e.jsx(x,{label:t,description:"All tones in the family",minHeight:"160px",children:e.jsx("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(150px, 1fr))",gap:"10px"},children:Object.entries(o).map(([a,d])=>e.jsxs("div",{style:{borderRadius:"10px",overflow:"hidden",border:"1px solid var(--border)"},children:[e.jsx("div",{style:{height:"52px",background:d}}),e.jsxs("div",{style:{padding:"10px",fontFamily:"var(--velum-font-mono)",fontSize:"0.78rem"},children:[t,".",a]})]},a))})},t))})})};var n,i,s;r.parameters={...r.parameters,docs:{...(n=r.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1100px">
      <StateMatrix columns="1fr">
        {Object.entries(colorFamilies).map(([family, values]) => <StateCase key={family} label={family} description="All tones in the family" minHeight="160px">
            <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
          gap: "10px"
        }}>
              {Object.entries(values).map(([tone, swatch]) => <div key={tone} style={{
            borderRadius: "10px",
            overflow: "hidden",
            border: "1px solid var(--border)"
          }}>
                  <div style={{
              height: "52px",
              background: swatch
            }} />
                  <div style={{
              padding: "10px",
              fontFamily: "var(--velum-font-mono)",
              fontSize: "0.78rem"
            }}>
                    {family}.{tone}
                  </div>
                </div>)}
            </div>
          </StateCase>)}
      </StateMatrix>
    </StoryFrame>
}`,...(s=(i=r.parameters)==null?void 0:i.docs)==null?void 0:s.source}}};const y=["Showcase"];export{r as Showcase,y as __namedExportsOrder,v as default};
