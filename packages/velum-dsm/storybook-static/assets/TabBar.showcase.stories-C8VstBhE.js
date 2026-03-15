import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as m}from"./index-hZsgmmNh.js";import{T as c}from"./VelumProvider-Cnx-m3OC.js";import{S as x,a as y,b as r}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const h={title:"Components/TabBar"};function i(t){const[l,p]=m.useState(t.activeKey);return e.jsx(c,{ariaLabel:"Example tabs",activeKey:l,onChange:p,layout:t.layout,size:t.size,items:[{key:"overview",label:"Overview"},{key:"spellbook",label:"Spellbook"},{key:"integrations",label:"Integrations"},{key:"history",label:"History",disabled:!0}]})}const a={render:()=>e.jsx(x,{maxWidth:"1080px",children:e.jsxs(y,{children:[e.jsx(r,{label:"Grid Layout",description:"Primary top-level navigation",minHeight:"120px",children:e.jsx(i,{activeKey:"overview",layout:"grid"})}),e.jsx(r,{label:"Wrapped Layout",description:"Compact sheet or subsection tabs",minHeight:"120px",children:e.jsx(i,{activeKey:"spellbook",layout:"wrap",size:"sm"})})]})})};var s,o,n;a.parameters={...a.parameters,docs:{...(s=a.parameters)==null?void 0:s.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1080px">
      <StateMatrix>
        <StateCase label="Grid Layout" description="Primary top-level navigation" minHeight="120px">
          <ExampleTabs activeKey="overview" layout="grid" />
        </StateCase>
        <StateCase label="Wrapped Layout" description="Compact sheet or subsection tabs" minHeight="120px">
          <ExampleTabs activeKey="spellbook" layout="wrap" size="sm" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(n=(o=a.parameters)==null?void 0:o.docs)==null?void 0:n.source}}};const g=["Showcase"];export{a as Showcase,g as __namedExportsOrder,h as default};
