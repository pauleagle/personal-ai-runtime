# FramePack Extraction Checklist

## Before Reading

- [x] Import upstream source into `external-source/FramePack/`
- [x] Record official repository and imported commit
- [x] Detect license file
- [ ] Run deeper copyright and notice review if deriving a playbook or skill

## Reading

- [ ] Read upstream `README.md`
- [ ] Review linked paper and project page
- [ ] Review install and runtime entry points
- [ ] Review GUI workflow and sanity-check guidance
- [ ] Review linked releases, issues, and discussions if needed

## Extraction

- [ ] Identify reusable high-level concepts
- [ ] Separate upstream-specific details from project-local rules
- [ ] Draft project-local summary
- [ ] Draft candidate checklist or playbook only if useful
- [ ] Add source attribution to any derived artifact

## Validation

- [ ] Verify command examples against the current upstream commit before recommending live usage
- [ ] Confirm model download and hardware requirements before any local experiment
- [ ] Avoid copying upstream examples, media, or long text into derived artifacts without license review
