import{j as e,y as i,z as o}from"./iframe-v_xVpIIQ.js";import{S as l,a as m,b as s,D as n}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const h={title:"Components/Layout/Section"},t={render:()=>e.jsx(l,{children:e.jsxs(m,{children:[e.jsx(s,{label:"Nested",description:"Section containing multiple subsections",minHeight:"260px",children:e.jsxs(i,{title:"Compendium Section",subtitle:"Top-level grouping for related content blocks.",children:[e.jsx(o,{title:"Primary Fields",children:e.jsx(n,{children:"Fields, summaries, and nested components can all live inside a section."})}),e.jsx(o,{title:"Secondary Fields",children:e.jsx(n,{children:"Sections are useful when the grouping matters more than a framed surface."})})]})}),e.jsx(s,{label:"Simple",description:"Section without nested hierarchy",minHeight:"180px",children:e.jsx(i,{title:"Simple Section",children:e.jsx(n,{children:"Use a section when structure matters more than chrome."})})})]})})};var r,a,c;t.parameters={...t.parameters,docs:{...(r=t.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => <StoryFrame>
      <StateMatrix>
        <StateCase label="Nested" description="Section containing multiple subsections" minHeight="260px">
          <Section title="Compendium Section" subtitle="Top-level grouping for related content blocks.">
            <Subsection title="Primary Fields">
              <DemoBlock>Fields, summaries, and nested components can all live inside a section.</DemoBlock>
            </Subsection>
            <Subsection title="Secondary Fields">
              <DemoBlock>Sections are useful when the grouping matters more than a framed surface.</DemoBlock>
            </Subsection>
          </Section>
        </StateCase>
        <StateCase label="Simple" description="Section without nested hierarchy" minHeight="180px">
          <Section title="Simple Section">
            <DemoBlock>Use a section when structure matters more than chrome.</DemoBlock>
          </Section>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(c=(a=t.parameters)==null?void 0:a.docs)==null?void 0:c.source}}};const p=["Showcase"];export{t as Showcase,p as __namedExportsOrder,h as default};
