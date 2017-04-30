from numpy import linalg, array, zeros


def triangulate_point(x1, x2, p1, p2):
    """Given two image coordinates x1, x2 of the same point X under different
    projections P1, P2, recovers X."""
    m = zeros((6, 6))
    m[:3, :4] = p1
    m[:3, 4] = -x1

    m[3:, :4] = p2
    m[3:, 5] = -x2  # Intentionally 5, not 4.

    u, s, v = linalg.svd(m)
    x = v[-1, :4]
    return x / x[3]


def triangulate(x1, x2, p1, p2):
    # Given n pairs of points, returns their 3d coordinates.
    n = x1.shape[1]
    if x2.shape[1] != n:
        raise ValueError('Number of points do not match.')
    x = [triangulate_point(x1[:, i], x2[:, i], p1, p2) for i in range(n)]
    return array(x).T
