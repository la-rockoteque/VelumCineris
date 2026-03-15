import{j as t}from"./jsx-runtime-Bll8AAhy.js";import{r as m}from"./index-hZsgmmNh.js";import{D as s}from"./VelumProvider-Cnx-m3OC.js";import{S as l}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const F={title:"Components/DelimitedListField",component:s,args:{value:"",onChange:()=>{}}},e={render:()=>{const[n,i]=m.useState("Fire, Cold");return t.jsx(l,{maxWidth:"980px",children:t.jsx(s,{value:n,options:["Fire","Cold","Lightning","Poison"],onChange:i})})}};var r,o,a;e.parameters={...e.parameters,docs:{...(r=e.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("Fire, Cold");
    return <StoryFrame maxWidth="980px">
        <DelimitedListField value={value} options={["Fire", "Cold", "Lightning", "Poison"]} onChange={setValue} />
      </StoryFrame>;
  }
}`,...(a=(o=e.parameters)==null?void 0:o.docs)==null?void 0:a.source}}};const g=["Default"];export{e as Default,g as __namedExportsOrder,F as default};
