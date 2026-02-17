shop = {
    # animal: (specie, descriptions)
    "parrot": ("Norvegian blue", ("restin'", "remarkable", "beautiful plumage")),
}

if "parrot" in shop is "restin'":  # [bad-chained-comparison]
    print("Hellooooo, Pooolllllyyy ! WAAAAKEEY, WAKKEEEY !")


def xor_check(*, left=None, right=None):
    if left is None != right is None:  # [bad-chained-comparison]
        raise ValueError(
            "Either both left= and right= need to be provided or none should."
        )
