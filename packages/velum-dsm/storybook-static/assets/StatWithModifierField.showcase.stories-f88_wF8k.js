import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as p}from"./index-hZsgmmNh.js";import{h as m}from"./VelumProvider-Cnx-m3OC.js";import{S as c,a as x,b as t}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const C={title:"Components/StatWithModifierField"};function a(s){const[l,d]=p.useState(s.initialValue);return e.jsx(m,{value:l,onChange:d})}const i={render:()=>e.jsx(c,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(t,{label:"Positive Modifier",description:"Standard ability score compound field",minHeight:"120px",children:e.jsx(a,{initialValue:"14"})}),e.jsx(t,{label:"Zero Modifier",description:"Centerline score",minHeight:"120px",children:e.jsx(a,{initialValue:"10"})}),e.jsx(t,{label:"Negative Modifier",description:"Low-score presentation",minHeight:"120px",children:e.jsx(a,{initialValue:"7"})})]})})};var r,n,o;i.parameters={...i.parameters,docs:{...(r=i.parameters)==null?void 0:r.docs,source:{originalSource:`{
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
}`,...(o=(n=i.parameters)==null?void 0:n.docs)==null?void 0:o.source}}};const M=["Showcase"];export{i as Showcase,M as __namedExportsOrder,C as default};
