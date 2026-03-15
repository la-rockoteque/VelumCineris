import{j as e,f as p,x as c}from"./iframe-v_xVpIIQ.js";import{S as x,a as m,b as t}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const f={title:"Components/StatWithModifierField"};function a(o){const[l,d]=p.useState(o.initialValue);return e.jsx(c,{value:l,onChange:d})}const i={render:()=>e.jsx(x,{maxWidth:"980px",children:e.jsxs(m,{children:[e.jsx(t,{label:"Positive Modifier",description:"Standard ability score compound field",minHeight:"120px",children:e.jsx(a,{initialValue:"14"})}),e.jsx(t,{label:"Zero Modifier",description:"Centerline score",minHeight:"120px",children:e.jsx(a,{initialValue:"10"})}),e.jsx(t,{label:"Negative Modifier",description:"Low-score presentation",minHeight:"120px",children:e.jsx(a,{initialValue:"7"})})]})})};var r,n,s;i.parameters={...i.parameters,docs:{...(r=i.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Positive Modifier" description="Standard ability score compound field" minHeight="120px">
          <Example initialValue="14" />
        </StateCase>
        <StateCase label="Zero Modifier" description="Centerline score" minHeight="120px">
          <Example initialValue="10" />
        </StateCase>
        <StateCase label="Negative Modifier" description="Low-score presentation" minHeight="120px">
          <Example initialValue="7" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(s=(n=i.parameters)==null?void 0:n.docs)==null?void 0:s.source}}};const j=["Showcase"];export{i as Showcase,j as __namedExportsOrder,f as default};
