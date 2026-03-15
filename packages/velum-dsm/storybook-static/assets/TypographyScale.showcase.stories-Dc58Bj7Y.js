import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{U as r}from"./VelumProvider-Cnx-m3OC.js";import{S as p,a as m,b as c}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const h={title:"Tokens/TypographyScale"},a={render:()=>e.jsx(p,{maxWidth:"980px",children:e.jsx(m,{columns:"1fr",children:Object.entries(r.size).map(([t,n])=>e.jsx(c,{label:t,description:`font-size ${n}`,minHeight:"140px",children:e.jsxs("div",{style:{fontFamily:r.display,fontSize:n,letterSpacing:r.tracking.normal,textTransform:"uppercase"},children:[t," heading sample"]})},t))})})};var s,o,i;a.parameters={...a.parameters,docs:{...(s=a.parameters)==null?void 0:s.docs,source:{originalSource:`{
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
}`,...(i=(o=a.parameters)==null?void 0:o.docs)==null?void 0:i.source}}};const f=["Showcase"];export{a as Showcase,f as __namedExportsOrder,h as default};
