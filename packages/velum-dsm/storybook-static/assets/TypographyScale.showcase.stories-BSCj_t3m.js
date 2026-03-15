import{j as e,t as r}from"./iframe-v_xVpIIQ.js";import{S as p,a as c,b as l}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const y={title:"Tokens/TypographyScale"},a={render:()=>e.jsx(p,{maxWidth:"980px",children:e.jsx(c,{columns:"1fr",children:Object.entries(r.size).map(([t,n])=>e.jsx(l,{label:t,description:`font-size ${n}`,minHeight:"140px",children:e.jsxs("div",{style:{fontFamily:r.display,fontSize:n,letterSpacing:r.tracking.normal,textTransform:"uppercase"},children:[t," heading sample"]})},t))})})};var s,i,o;a.parameters={...a.parameters,docs:{...(s=a.parameters)==null?void 0:s.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix columns="1fr">
        {Object.entries(typographyScale.size).map(([token, value]) => <StateCase key={token} label={token} description={\`font-size \${value}\`} minHeight="140px">
            <div style={{
          fontFamily: typographyScale.display,
          fontSize: value,
          letterSpacing: typographyScale.tracking.normal,
          textTransform: "uppercase"
        }}>
              {token} heading sample
            </div>
          </StateCase>)}
      </StateMatrix>
    </StoryFrame>
}`,...(o=(i=a.parameters)==null?void 0:i.docs)==null?void 0:o.source}}};const x=["Showcase"];export{a as Showcase,x as __namedExportsOrder,y as default};
