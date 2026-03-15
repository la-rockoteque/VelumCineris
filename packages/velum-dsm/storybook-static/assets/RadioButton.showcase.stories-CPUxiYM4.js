import{j as e,h as a}from"./iframe-v_xVpIIQ.js";import{S as d,a as l,b as t}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const b={title:"Components/RadioButton"},i={render:()=>e.jsx(d,{maxWidth:"980px",children:e.jsxs(l,{children:[e.jsx(t,{label:"Unchecked",description:"Available radio option",children:e.jsx(a,{name:"publish-mode-a",label:"Dry Run"})}),e.jsx(t,{label:"Checked",description:"Selected radio option",children:e.jsx(a,{name:"publish-mode-b",label:"Live Execute",checked:!0,readOnly:!0})}),e.jsx(t,{label:"With Description",description:"Additional context",children:e.jsx(a,{name:"publish-mode-c",label:"Publish and Sync",description:"Use when all linked destinations should receive updates."})}),e.jsx(t,{label:"Disabled",description:"Unavailable option",children:e.jsx(a,{name:"publish-mode-d",label:"Locked",disabled:!0})})]})})};var n,o,s;i.parameters={...i.parameters,docs:{...(n=i.parameters)==null?void 0:n.docs,source:{originalSource:`{
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
}`,...(s=(o=i.parameters)==null?void 0:o.docs)==null?void 0:s.source}}};const m=["Showcase"];export{i as Showcase,m as __namedExportsOrder,b as default};
