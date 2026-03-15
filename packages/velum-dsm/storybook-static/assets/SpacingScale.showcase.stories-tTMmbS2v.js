import{j as r}from"./jsx-runtime-Bll8AAhy.js";import{O as n}from"./VelumProvider-Cnx-m3OC.js";import{S as o,a as l,b as i}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const u={title:"Tokens/SpacingScale"},d={render:()=>r.jsx(o,{maxWidth:"980px",children:r.jsxs(l,{children:[r.jsx(i,{label:"Compact",description:"Steps 0-3",minHeight:"180px",children:r.jsx("div",{style:{display:"grid",gap:"8px"},children:Object.entries(n).filter(([e])=>Number(e)<=3).map(([e,a])=>r.jsx("div",{style:{border:"1px solid var(--border)",borderRadius:"12px",padding:a,background:"var(--surface)"},children:r.jsxs("div",{style:{border:"1px dashed var(--accent)",borderRadius:"8px",padding:"8px",fontFamily:"var(--velum-font-mono)"},children:[e," = ",a]})},e))})}),r.jsx(i,{label:"Standard",description:"Steps 4-6",minHeight:"220px",children:r.jsx("div",{style:{display:"grid",gap:"8px"},children:Object.entries(n).filter(([e])=>Number(e)>=4&&Number(e)<=6).map(([e,a])=>r.jsx("div",{style:{border:"1px solid var(--border)",borderRadius:"12px",padding:a,background:"var(--surface)"},children:r.jsxs("div",{style:{border:"1px dashed var(--accent)",borderRadius:"8px",padding:"8px",fontFamily:"var(--velum-font-mono)"},children:[e," = ",a]})},e))})}),r.jsx(i,{label:"Large",description:"Steps 7-9",minHeight:"260px",children:r.jsx("div",{style:{display:"grid",gap:"8px"},children:Object.entries(n).filter(([e])=>Number(e)>=7).map(([e,a])=>r.jsx("div",{style:{border:"1px solid var(--border)",borderRadius:"12px",padding:a,background:"var(--surface)"},children:r.jsxs("div",{style:{border:"1px dashed var(--accent)",borderRadius:"8px",padding:"8px",fontFamily:"var(--velum-font-mono)"},children:[e," = ",a]})},e))})})]})})};var s,t,p;d.parameters={...d.parameters,docs:{...(s=d.parameters)==null?void 0:s.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Compact" description="Steps 0-3" minHeight="180px">
          <div style={{
          display: "grid",
          gap: "8px"
        }}>
            {Object.entries(spacingScale).filter(([step]) => Number(step) <= 3).map(([step, value]) => <div key={step} style={{
            border: "1px solid var(--border)",
            borderRadius: "12px",
            padding: value,
            background: "var(--surface)"
          }}>
                  <div style={{
              border: "1px dashed var(--accent)",
              borderRadius: "8px",
              padding: "8px",
              fontFamily: "var(--velum-font-mono)"
            }}>
                    {step} = {value}
                  </div>
                </div>)}
          </div>
        </StateCase>
        <StateCase label="Standard" description="Steps 4-6" minHeight="220px">
          <div style={{
          display: "grid",
          gap: "8px"
        }}>
            {Object.entries(spacingScale).filter(([step]) => Number(step) >= 4 && Number(step) <= 6).map(([step, value]) => <div key={step} style={{
            border: "1px solid var(--border)",
            borderRadius: "12px",
            padding: value,
            background: "var(--surface)"
          }}>
                  <div style={{
              border: "1px dashed var(--accent)",
              borderRadius: "8px",
              padding: "8px",
              fontFamily: "var(--velum-font-mono)"
            }}>
                    {step} = {value}
                  </div>
                </div>)}
          </div>
        </StateCase>
        <StateCase label="Large" description="Steps 7-9" minHeight="260px">
          <div style={{
          display: "grid",
          gap: "8px"
        }}>
            {Object.entries(spacingScale).filter(([step]) => Number(step) >= 7).map(([step, value]) => <div key={step} style={{
            border: "1px solid var(--border)",
            borderRadius: "12px",
            padding: value,
            background: "var(--surface)"
          }}>
                  <div style={{
              border: "1px dashed var(--accent)",
              borderRadius: "8px",
              padding: "8px",
              fontFamily: "var(--velum-font-mono)"
            }}>
                    {step} = {value}
                  </div>
                </div>)}
          </div>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(p=(t=d.parameters)==null?void 0:t.docs)==null?void 0:p.source}}};const g=["Showcase"];export{d as Showcase,g as __namedExportsOrder,u as default};
