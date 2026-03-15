import{j as t,C as e,M as o,A as l,b as n}from"./iframe-v_xVpIIQ.js";import{S as c,a as m,b as i}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const u={title:"Components/Layout/Card"},a={render:()=>t.jsx(c,{maxWidth:"980px",children:t.jsxs(m,{children:[t.jsx(i,{label:"Standard",description:"Title, subtitle, metadata, and actions",minHeight:"220px",children:t.jsxs(e,{title:"Editorial Card",subtitle:"Standard framed content.",children:[t.jsx(o,{children:"Cards can host summary text, metadata, and nested actions."}),t.jsxs(l,{children:[t.jsx(n,{$variant:"primary",children:"Publish"}),t.jsx(n,{children:"Preview"})]})]})}),t.jsx(i,{label:"Title Only",description:"Subtitle is optional",minHeight:"220px",children:t.jsx(e,{title:"No Subtitle",children:t.jsx("p",{style:{margin:0},children:"The subtitle is optional, and cards still keep a stable internal rhythm."})})})]})})};var r,s,d;a.parameters={...a.parameters,docs:{...(r=a.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Standard" description="Title, subtitle, metadata, and actions" minHeight="220px">
          <Card title="Editorial Card" subtitle="Standard framed content.">
            <MetaText>Cards can host summary text, metadata, and nested actions.</MetaText>
            <ActionRow>
              <Button $variant="primary">Publish</Button>
              <Button>Preview</Button>
            </ActionRow>
          </Card>
        </StateCase>
        <StateCase label="Title Only" description="Subtitle is optional" minHeight="220px">
          <Card title="No Subtitle">
            <p style={{
            margin: 0
          }}>The subtitle is optional, and cards still keep a stable internal rhythm.</p>
          </Card>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(d=(s=a.parameters)==null?void 0:s.docs)==null?void 0:d.source}}};const S=["Showcase"];export{a as Showcase,S as __namedExportsOrder,u as default};
