import{j as e,f as p,w as m}from"./iframe-v_xVpIIQ.js";import{S as d,a as x,b as a}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const F={title:"Components/MultiSelect"};function i(n){const[o,c]=p.useState(n.initialValue);return e.jsx(m,{value:o,onChange:c,options:["Fire","Cold","Force","Necrotic","Radiant"],placeholder:"Pick tags"})}const t={render:()=>e.jsx(d,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(a,{label:"Empty",description:"Prompt-first enum picker",minHeight:"120px",children:e.jsx(i,{initialValue:""})}),e.jsx(a,{label:"Selected Tags",description:"Shows selected items as pills",minHeight:"120px",children:e.jsx(i,{initialValue:"Fire, Force"})}),e.jsx(a,{label:"Many Values",description:"Wraps pills inside the same control shell",minHeight:"120px",children:e.jsx(i,{initialValue:"Fire, Cold, Force, Necrotic"})})]})})};var s,r,l;t.parameters={...t.parameters,docs:{...(s=t.parameters)==null?void 0:s.docs,source:{originalSource:`{
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
}`,...(l=(r=t.parameters)==null?void 0:r.docs)==null?void 0:l.source}}};const C=["Showcase"];export{t as Showcase,C as __namedExportsOrder,F as default};
