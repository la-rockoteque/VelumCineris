import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as d}from"./index-hZsgmmNh.js";import{N as p}from"./VelumProvider-Cnx-m3OC.js";import{S as x,a as c,b as a}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const b={title:"Components/NamedTableField"};function r(o){const[l,m]=d.useState(o.initialValue);return e.jsx(p,{value:l,keyLabel:"Title",valueLabel:"Text",onChange:m})}const t={render:()=>e.jsx(x,{maxWidth:"1240px",children:e.jsxs(c,{columns:"1fr",children:[e.jsx(a,{label:"Trait Rows",description:"Compound row editor with glued cells",minHeight:"280px",children:e.jsx(r,{initialValue:"Trait:: Extra damage; Burst:: Pushes the target 10 feet"})}),e.jsx(a,{label:"Single Blank Row",description:"Starts with one editable row when there is no serialized data",minHeight:"220px",children:e.jsx(r,{initialValue:""})})]})})};var i,s,n;t.parameters={...t.parameters,docs:{...(i=t.parameters)==null?void 0:i.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1240px">
      <StateMatrix columns="1fr">
        <StateCase label="Trait Rows" description="Compound row editor with glued cells" minHeight="280px">
          <Example initialValue="Trait:: Extra damage; Burst:: Pushes the target 10 feet" />
        </StateCase>
        <StateCase label="Single Blank Row" description="Starts with one editable row when there is no serialized data" minHeight="220px">
          <Example initialValue="" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(n=(s=t.parameters)==null?void 0:s.docs)==null?void 0:n.source}}};const f=["Showcase"];export{t as Showcase,f as __namedExportsOrder,b as default};
