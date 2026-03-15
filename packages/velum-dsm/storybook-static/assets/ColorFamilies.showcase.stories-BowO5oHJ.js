import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{H as l}from"./VelumProvider-Cnx-m3OC.js";import{S as m,a as p,b as x}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const u={title:"Tokens/ColorFamilies"},r={render:()=>e.jsx(m,{maxWidth:"1100px",children:e.jsx(p,{columns:"1fr",children:Object.entries(l).map(([t,s])=>e.jsx(x,{label:t,description:"All tones in the family",minHeight:"160px",children:e.jsx("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(150px, 1fr))",gap:"10px"},children:Object.entries(s).map(([a,d])=>e.jsxs("div",{style:{borderRadius:"10px",overflow:"hidden",border:"1px solid var(--border)"},children:[e.jsx("div",{style:{height:"52px",background:d}}),e.jsxs("div",{style:{padding:"10px",fontFamily:"var(--velum-font-mono)",fontSize:"0.78rem"},children:[t,".",a]})]},a))})},t))})})};var i,n,o;r.parameters={...r.parameters,docs:{...(i=r.parameters)==null?void 0:i.docs,source:{originalSource:`{
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
}`,...(o=(n=r.parameters)==null?void 0:n.docs)==null?void 0:o.source}}};const b=["Showcase"];export{r as Showcase,b as __namedExportsOrder,u as default};
