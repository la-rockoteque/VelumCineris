import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as m}from"./index-hZsgmmNh.js";import{d}from"./VelumProvider-Cnx-m3OC.js";import{S as c,a as x,b as a}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const j={title:"Components/ComponentsField"};function i(l){const[o,p]=m.useState(l.initialValue);return e.jsx(d,{value:o,onChange:p})}const t={render:()=>e.jsx(c,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(a,{label:"Empty",description:"No components selected",minHeight:"150px",children:e.jsx(i,{initialValue:""})}),e.jsx(a,{label:"Verbal and Somatic",description:"Common spell setup",minHeight:"150px",children:e.jsx(i,{initialValue:"V, S"})}),e.jsx(a,{label:"Material Note",description:"Supports material details",minHeight:"150px",children:e.jsx(i,{initialValue:"V, M (a pearl worth 100 gp)"})})]})})};var r,n,s;t.parameters={...t.parameters,docs:{...(r=t.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Empty" description="No components selected" minHeight="150px">
          <ExampleField initialValue="" />
        </StateCase>
        <StateCase label="Verbal and Somatic" description="Common spell setup" minHeight="150px">
          <ExampleField initialValue="V, S" />
        </StateCase>
        <StateCase label="Material Note" description="Supports material details" minHeight="150px">
          <ExampleField initialValue="V, M (a pearl worth 100 gp)" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(s=(n=t.parameters)==null?void 0:n.docs)==null?void 0:s.source}}};const g=["Showcase"];export{t as Showcase,g as __namedExportsOrder,j as default};
