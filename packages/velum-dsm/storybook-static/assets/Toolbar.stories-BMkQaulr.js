import{j as r}from"./jsx-runtime-Bll8AAhy.js";import{x as o,g as n,l as s}from"./VelumProvider-Cnx-m3OC.js";import{S as p}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const x={title:"Patterns/Toolbar",component:o},e={render:()=>r.jsx(p,{maxWidth:"960px",children:r.jsxs(o,{children:[r.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Source",r.jsxs(n,{defaultValue:"translator",children:[r.jsx("option",{value:"translator",children:"Translator"}),r.jsx("option",{value:"formatter",children:"Formatter"})]})]}),r.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Filter",r.jsx(s,{defaultValue:"Archive"})]})]})})};var t,a,l;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="960px">
      <Toolbar>
        <label style={{
        display: "grid",
        gap: "8px"
      }}>
          Source
          <SelectInput defaultValue="translator">
            <option value="translator">Translator</option>
            <option value="formatter">Formatter</option>
          </SelectInput>
        </label>
        <label style={{
        display: "grid",
        gap: "8px"
      }}>
          Filter
          <TextInput defaultValue="Archive" />
        </label>
      </Toolbar>
    </StoryFrame>
}`,...(l=(a=e.parameters)==null?void 0:a.docs)==null?void 0:l.source}}};const f=["Default"];export{e as Default,f as __namedExportsOrder,x as default};
