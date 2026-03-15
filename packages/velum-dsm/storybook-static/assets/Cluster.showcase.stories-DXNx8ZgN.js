import{j as t,F as n,b as e}from"./iframe-v_xVpIIQ.js";import{S as d,a as c,b as r}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const x={title:"Components/Layout/Cluster"},a={render:()=>t.jsx(d,{children:t.jsxs(c,{children:[t.jsx(r,{label:"Wrapped Actions",description:"Cluster handles mixed-width actions",children:t.jsxs(n,{$gap:2,children:[t.jsx(e,{$variant:"primary",children:"Translate"}),t.jsx(e,{children:"Reload Context"}),t.jsx(e,{$variant:"ghost",children:"Pronunciation"}),t.jsx(e,{disabled:!0,children:"Disabled"})]})}),t.jsx(r,{label:"Spaced Between",description:"Can distribute content across a row",children:t.jsxs(n,{$gap:2,$justify:"space-between",children:[t.jsx(e,{children:"Back"}),t.jsx(e,{$variant:"primary",children:"Continue"})]})})]})})};var s,o,i;a.parameters={...a.parameters,docs:{...(s=a.parameters)==null?void 0:s.docs,source:{originalSource:`{
  render: () => <StoryFrame>
      <StateMatrix>
        <StateCase label="Wrapped Actions" description="Cluster handles mixed-width actions">
          <Cluster $gap={2}>
            <Button $variant="primary">Translate</Button>
            <Button>Reload Context</Button>
            <Button $variant="ghost">Pronunciation</Button>
            <Button disabled>Disabled</Button>
          </Cluster>
        </StateCase>
        <StateCase label="Spaced Between" description="Can distribute content across a row">
          <Cluster $gap={2} $justify="space-between">
            <Button>Back</Button>
            <Button $variant="primary">Continue</Button>
          </Cluster>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(i=(o=a.parameters)==null?void 0:o.docs)==null?void 0:i.source}}};const m=["Showcase"];export{a as Showcase,m as __namedExportsOrder,x as default};
