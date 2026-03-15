import{j as e,f as m,u as d}from"./iframe-v_xVpIIQ.js";import{S as c,a as x,b as a}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const V={title:"Components/ComponentsField"};function i(r){const[o,p]=m.useState(r.initialValue);return e.jsx(d,{value:o,onChange:p})}const t={render:()=>e.jsx(c,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(a,{label:"Empty",description:"No components selected",minHeight:"150px",children:e.jsx(i,{initialValue:""})}),e.jsx(a,{label:"Verbal and Somatic",description:"Common spell setup",minHeight:"150px",children:e.jsx(i,{initialValue:"V, S"})}),e.jsx(a,{label:"Material Note",description:"Supports material details",minHeight:"150px",children:e.jsx(i,{initialValue:"V, M (a pearl worth 100 gp)"})})]})})};var n,s,l;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`{
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
}`,...(l=(s=t.parameters)==null?void 0:s.docs)==null?void 0:l.source}}};const C=["Showcase"];export{t as Showcase,C as __namedExportsOrder,V as default};
