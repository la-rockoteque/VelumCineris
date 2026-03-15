import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{f as a}from"./VelumProvider-Cnx-m3OC.js";import{S as d,a as l,b as t}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const h={title:"Components/RadioButton"},i={render:()=>e.jsx(d,{maxWidth:"980px",children:e.jsxs(l,{children:[e.jsx(t,{label:"Unchecked",description:"Available radio option",children:e.jsx(a,{name:"publish-mode-a",label:"Dry Run"})}),e.jsx(t,{label:"Checked",description:"Selected radio option",children:e.jsx(a,{name:"publish-mode-b",label:"Live Execute",checked:!0,readOnly:!0})}),e.jsx(t,{label:"With Description",description:"Additional context",children:e.jsx(a,{name:"publish-mode-c",label:"Publish and Sync",description:"Use when all linked destinations should receive updates."})}),e.jsx(t,{label:"Disabled",description:"Unavailable option",children:e.jsx(a,{name:"publish-mode-d",label:"Locked",disabled:!0})})]})})};var n,o,s;i.parameters={...i.parameters,docs:{...(n=i.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Unchecked" description="Available radio option">
          <RadioButton name="publish-mode-a" label="Dry Run" />
        </StateCase>
        <StateCase label="Checked" description="Selected radio option">
          <RadioButton name="publish-mode-b" label="Live Execute" checked readOnly />
        </StateCase>
        <StateCase label="With Description" description="Additional context">
          <RadioButton name="publish-mode-c" label="Publish and Sync" description="Use when all linked destinations should receive updates." />
        </StateCase>
        <StateCase label="Disabled" description="Unavailable option">
          <RadioButton name="publish-mode-d" label="Locked" disabled />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(s=(o=i.parameters)==null?void 0:o.docs)==null?void 0:s.source}}};const u=["Showcase"];export{i as Showcase,u as __namedExportsOrder,h as default};
