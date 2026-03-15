import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as p}from"./index-hZsgmmNh.js";import{M as m}from"./VelumProvider-Cnx-m3OC.js";import{S as d,a as x,b as a}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const g={title:"Components/MultiSelect"};function i(n){const[o,c]=p.useState(n.initialValue);return e.jsx(m,{value:o,onChange:c,options:["Fire","Cold","Force","Necrotic","Radiant"],placeholder:"Pick tags"})}const t={render:()=>e.jsx(d,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(a,{label:"Empty",description:"Prompt-first enum picker",minHeight:"120px",children:e.jsx(i,{initialValue:""})}),e.jsx(a,{label:"Selected Tags",description:"Shows selected items as pills",minHeight:"120px",children:e.jsx(i,{initialValue:"Fire, Force"})}),e.jsx(a,{label:"Many Values",description:"Wraps pills inside the same control shell",minHeight:"120px",children:e.jsx(i,{initialValue:"Fire, Cold, Force, Necrotic"})})]})})};var s,r,l;t.parameters={...t.parameters,docs:{...(s=t.parameters)==null?void 0:s.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Empty" description="Prompt-first enum picker" minHeight="120px">
          <Example initialValue="" />
        </StateCase>
        <StateCase label="Selected Tags" description="Shows selected items as pills" minHeight="120px">
          <Example initialValue="Fire, Force" />
        </StateCase>
        <StateCase label="Many Values" description="Wraps pills inside the same control shell" minHeight="120px">
          <Example initialValue="Fire, Cold, Force, Necrotic" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(l=(r=t.parameters)==null?void 0:r.docs)==null?void 0:l.source}}};const j=["Showcase"];export{t as Showcase,j as __namedExportsOrder,g as default};
