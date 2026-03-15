import{j as e,f as m,N as x}from"./iframe-v_xVpIIQ.js";import{S as p,a as c,b as a}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const w={title:"Components/NamedTableField"};function i(l){const[o,d]=m.useState(l.initialValue);return e.jsx(x,{value:o,keyLabel:"Title",valueLabel:"Text",onChange:d})}const t={render:()=>e.jsx(p,{maxWidth:"1240px",children:e.jsxs(c,{columns:"1fr",children:[e.jsx(a,{label:"Trait Rows",description:"Compound row editor with glued cells",minHeight:"280px",children:e.jsx(i,{initialValue:"Trait:: Extra damage; Burst:: Pushes the target 10 feet"})}),e.jsx(a,{label:"Single Blank Row",description:"Starts with one editable row when there is no serialized data",minHeight:"220px",children:e.jsx(i,{initialValue:""})})]})})};var r,s,n;t.parameters={...t.parameters,docs:{...(r=t.parameters)==null?void 0:r.docs,source:{originalSource:`{
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
}`,...(n=(s=t.parameters)==null?void 0:s.docs)==null?void 0:n.source}}};const g=["Showcase"];export{t as Showcase,g as __namedExportsOrder,w as default};
