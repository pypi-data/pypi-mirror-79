def __match(pattern, value):
    import re
    return any(re.match(p, value) for p in pattern.split(","))


def match_area(matchers, area_std, area_3rd):
    return any(m(area_std, area_3rd) for m in matchers)


def load_matcher(config):
    def _f(area_std, area_3rd):
        assert len(area_std) == 3
        assert len(area_3rd) == 3
        patterns_std = config["pattern_std"].split("|")
        assert len(patterns_std) == 3
        patterns_3rd = config["pattern_3rd"].split("|")
        assert len(patterns_3rd) == 3
        args = {"province": area_std[0],
                "city": area_std[1], "district": area_std[2]}
        return all(__match(pattern, area) for pattern, area in zip(patterns_std, area_std)) and all(__match(pattern.format(**args), area) for pattern, area in zip(patterns_3rd, area_3rd))
    return _f


def load_matchers(path):
    import zzpy as z
    return [load_matcher(config) for config in z.read_jsonline(path)]


def main():
    matcher = load_matcher(
        {"pattern_std": "重庆市|.*|.*", "pattern_3rd": "重庆市|.*|.*"})
    print(matcher(("重庆市", "asdf", "123"), ("重庆市", "xxx", "qqq")))
    
    matcher = load_matcher(
        {"pattern_std": ".*|.*|.*", "pattern_3rd": "{province}|{city}|.*"})
    print(matcher(("重庆市", "asdf", "123"), ("重庆市", "xxx", "qqq")))
    print(matcher(("重庆市", "asdf", "123"), ("重庆市", "asdf", "qqq")))


if __name__ == "__main__":
    main()
