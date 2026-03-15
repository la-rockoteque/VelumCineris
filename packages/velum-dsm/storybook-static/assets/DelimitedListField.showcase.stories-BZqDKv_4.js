import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as d}from"./index-hZsgmmNh.js";import{D as p}from"./VelumProvider-Cnx-m3OC.js";import{S as x,a as c,b as a}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const w={title:"Components/DelimitedListField"};function s(i){const[l,m]=d.useState(i.initialValue);return e.jsx(p,{value:l,onChange:m,options:i.options})}const t={render:()=>e.jsx(x,{maxWidth:"1080px",children:e.jsxs(c,{columns:"1fr",children:[e.jsx(a,{label:"Suggested Values",description:"Editable rows with datalist suggestions",minHeight:"220px",children:e.jsx(s,{initialValue:"Fire, Cold",options:["Fire","Cold","Lightning","Poison"]})}),e.jsx(a,{label:"Blank List",description:"Begins with a single empty editable row",minHeight:"180px",children:e.jsx(s,{initialValue:""})})]})})};var n,r,o;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1080px">
      <StateMatrix columns="1fr">
        <StateCase label="Suggested Values" description="Editable rows with datalist suggestions" minHeight="220px">
          <Example initialValue="Fire, Cold" options={["Fire", "Cold", "Lightning", "Poison"]} />
        </StateCase>
        <StateCase label="Blank List" description="Begins with a single empty editable row" minHeight="180px">
          <Example initialValue="" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(o=(r=t.parameters)==null?void 0:r.docs)==null?void 0:o.source}}};const b=["Showcase"];export{t as Showcase,b as __namedExportsOrder,w as default};
