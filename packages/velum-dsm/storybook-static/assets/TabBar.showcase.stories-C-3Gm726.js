import{j as e,f as m,o as p}from"./iframe-v_xVpIIQ.js";import{S as x,a as d,b as s}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const h={title:"Components/TabBar"};function r(a){const[n,c]=m.useState(a.activeKey);return e.jsx(p,{ariaLabel:"Example tabs",activeKey:n,onChange:c,layout:a.layout,size:a.size,items:[{key:"spells",label:"Spells"},{key:"monsters",label:"Monsters"},{key:"feats",label:"Feats"},{key:"species",label:"Species",disabled:!0}]})}const t={render:()=>e.jsx(x,{maxWidth:"1080px",children:e.jsxs(d,{children:[e.jsx(s,{label:"Sheet Selector",description:"Default stepped sheet tabs",minHeight:"120px",children:e.jsx(r,{activeKey:"spells",layout:"grid"})}),e.jsx(s,{label:"Compact Tabs",description:"Smaller tab treatment for dense spaces",minHeight:"120px",children:e.jsx(r,{activeKey:"monsters",layout:"wrap",size:"sm"})})]})})};var i,l,o;t.parameters={...t.parameters,docs:{...(i=t.parameters)==null?void 0:i.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1080px">
      <StateMatrix>
        <StateCase label="Sheet Selector" description="Default stepped sheet tabs" minHeight="120px">
          <ExampleTabs activeKey="spells" layout="grid" />
        </StateCase>
        <StateCase label="Compact Tabs" description="Smaller tab treatment for dense spaces" minHeight="120px">
          <ExampleTabs activeKey="monsters" layout="wrap" size="sm" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(o=(l=t.parameters)==null?void 0:l.docs)==null?void 0:o.source}}};const u=["Showcase"];export{t as Showcase,u as __namedExportsOrder,h as default};
