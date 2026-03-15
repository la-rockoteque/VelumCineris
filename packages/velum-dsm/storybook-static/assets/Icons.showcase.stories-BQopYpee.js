import{j as e,C as p,i as x}from"./iframe-v_xVpIIQ.js";import{S as l,a as o,b as c}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const g={title:"Assets/Icons"},s={render:()=>e.jsx(l,{maxWidth:"980px",children:e.jsx(p,{title:"Icons Showcase",subtitle:"Full icon set rendered across common sizing treatments.",children:e.jsx(o,{columns:"repeat(auto-fit, minmax(240px, 1fr))",children:Object.entries(x).map(([t,a])=>e.jsx(c,{label:t,description:"16px, 32px, 64px",minHeight:"120px",children:e.jsxs("div",{style:{display:"flex",alignItems:"center",gap:"16px",flexWrap:"wrap"},children:[e.jsx("img",{src:a,alt:`${t} 16`,style:{width:"16px",height:"16px"}}),e.jsx("img",{src:a,alt:`${t} 32`,style:{width:"32px",height:"32px"}}),e.jsx("img",{src:a,alt:`${t} 64`,style:{width:"64px",height:"64px"}})]})},t))})})})};var r,n,i;s.parameters={...s.parameters,docs:{...(r=s.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <Card title="Icons Showcase" subtitle="Full icon set rendered across common sizing treatments.">
        <StateMatrix columns="repeat(auto-fit, minmax(240px, 1fr))">
          {Object.entries(iconAssets).map(([name, url]) => <StateCase key={name} label={name} description="16px, 32px, 64px" minHeight="120px">
              <div style={{
            display: "flex",
            alignItems: "center",
            gap: "16px",
            flexWrap: "wrap"
          }}>
                <img src={url} alt={\`\${name} 16\`} style={{
              width: "16px",
              height: "16px"
            }} />
                <img src={url} alt={\`\${name} 32\`} style={{
              width: "32px",
              height: "32px"
            }} />
                <img src={url} alt={\`\${name} 64\`} style={{
              width: "64px",
              height: "64px"
            }} />
              </div>
            </StateCase>)}
        </StateMatrix>
      </Card>
    </StoryFrame>
}`,...(i=(n=s.parameters)==null?void 0:n.docs)==null?void 0:i.source}}};const u=["Showcase"];export{s as Showcase,u as __namedExportsOrder,g as default};
